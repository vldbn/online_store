import json
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from cart.forms import CartAddButton, CartAddForm
from store.forms import RatingForm
from store.models import Category, Product, Wish, Rating
from store.recommendations import Recommendations
from store.tasks import fit_model

recommendations_url = settings.RECOMMENDATIONS_URL
fit_url = settings.FIT_URL


class ProductListView(View):
    """Productlist view."""

    def get(self, request):
        categories = Category.objects.all()
        product_list = Product.objects.filter(available=True)
        paginator = Paginator(product_list, 6)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context = {
            'products': products,
            'categories': categories,
            'category': 'All categories'
        }
        return render(request, 'store/product_list.html', context)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        if 'wish' in request.POST:
            product_id = request.POST.get('wish')
            Wish.objects.create(
                user=user,
                product_id=product_id
            )
        elif 'del' in request.POST:
            product_id = request.POST.get('del')
            wishes = Wish.objects.filter(product_id=product_id)
            wish = wishes.filter(user_id=user.id)
            wish.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ProductCategoryListView(View):
    """Product list view by category."""

    def get(self, request, slug):
        categories = Category.objects.all()
        category = get_object_or_404(Category, slug=slug)
        product_list = Product.objects.filter(category=category)
        product_list = product_list.filter(available=True)
        paginator = Paginator(product_list, 6)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        form = CartAddButton()
        context = {
            'products': products,
            'categories': categories,
            'category': category,
            'form': form
        }
        return render(request, 'store/product_list.html', context)

    def post(self, request, slug):
        user = User.objects.get(id=request.user.id)
        if 'wish' in request.POST:
            product_id = request.POST.get('wish')
            Wish.objects.create(
                user=user,
                product_id=product_id
            )
        elif 'del' in request.POST:
            product_id = request.POST.get('del')
            wishes = Wish.objects.filter(product_id=product_id)
            wish = wishes.filter(user_id=user.id)
            wish.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ProductDetailView(View):
    """Product detail view."""

    r = Recommendations()

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        categories = Category.objects.all()

        form = CartAddForm()

        rating_form = RatingForm()

        recommended_products = self.r.suggest_products_for([product], 4)

        context = {
            'product': product,
            'categories': categories,
            'form': form,
            'rating_form': rating_form,
            'recommended_products': recommended_products
        }
        return render(request, 'store/product_detail.html', context)

    def post(self, request, slug):
        user = User.objects.get(id=request.user.id)
        product = Product.objects.get(slug=slug)
        rating_form = RatingForm(request.POST)

        if 'wish' in request.POST:
            product_id = request.POST.get('wish')
            Wish.objects.create(
                user=user,
                product_id=product_id
            )
        if 'del' in request.POST:
            product_id = request.POST.get('del')
            wishes = Wish.objects.filter(product_id=product_id)
            wish = wishes.filter(user_id=user.id)
            wish.delete()

        if rating_form.is_valid():
            rate = rating_form.cleaned_data.get('rate')
            try:
                ex_rate = Rating.objects.get(user=user, product=product)
            except ObjectDoesNotExist:
                ex_rate = None
            if ex_rate:
                ex_rate.rate = rate
                ex_rate.save()
                try:
                    fit_model.delay()
                except requests.ConnectionError:
                    print('Can not send request.')
            else:
                Rating.objects.create(
                    user=user,
                    product=product,
                    rate=rate
                )
                try:
                    fit_model.delay()
                except requests.ConnectionError:
                    print('Can not send request.')

        return redirect('store:product-detail', slug=slug)


class WishListView(LoginRequiredMixin, View):
    """Products wish list."""

    def get(self, request):
        categories = Category.objects.all()
        user = User.objects.get(id=request.user.id)
        wishes = Wish.objects.filter(user=user)
        wishes_id_list = [i.product_id for i in wishes]
        product_list = Product.objects.filter(id__in=wishes_id_list)
        paginator = Paginator(product_list, 6)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context = {
            'categories': categories,
            'products': products,
            'category': 'Wish list'
        }
        return render(request, 'store/product_list.html', context)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        if 'wish' in request.POST:
            product_id = request.POST.get('wish')
            Wish.objects.create(
                user=user,
                product_id=product_id
            )
        if 'del' in request.POST:
            product_id = request.POST.get('del')
            wishes = Wish.objects.filter(product_id=product_id)
            wish = wishes.filter(user_id=user.id)
            wish.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class RecommendationsView(LoginRequiredMixin, View):
    """Recommendations view makes post request with user_id and
    gets product id's."""

    def get(self, request, user_id):
        categories = Category.objects.all()
        user = User.objects.get(id=user_id)
        try:
            user_id = {'user_id': user.id}
            j = json.dumps(user_id)

            response = requests.post(recommendations_url, data=j)
            response = json.loads(response.json())

            rec_list = response['recommendations']
            products = []
            for i in rec_list:
                products.append(Product.objects.get(id=int(i)))

            context = {
                'categories': categories,
                'products': products,
                'category': 'Recommendations'
            }
        except json.JSONDecodeError:
            context = {
                'categories': categories,
                'products': [],
                'category': 'Recommendations'
            }

        return render(request, 'store/product_list.html', context)
