import json
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from cart.forms import CartAddButton, CartAddForm
from orders.models import OrderItem
from store.forms import RatingForm
from store.mixins import WishMixin
from store.models import Category, Product, Wish, Rating
from store.recommendations import Recommendations
from store.tasks import fit_model

recommendations_url = settings.RECOMMENDATIONS_URL
fit_url = settings.FIT_URL


class ProductListView(WishMixin, View):
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


class ProductCategoryListView(WishMixin, View):
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

                fit_model.delay()

            else:
                Rating.objects.create(
                    user=user,
                    product=product,
                    rate=rate
                )

                fit_model.delay()

        return redirect('store:product-detail', slug=slug)


class WishListView(LoginRequiredMixin, WishMixin, View):
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


class RecommendationsView(LoginRequiredMixin, WishMixin, View):
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


class BestsellingView(WishMixin, View):
    """Returns products sorted buy amount of purchases."""

    def get(self, request):
        categories = Category.objects.all()
        all_orders = OrderItem.objects.all()

        orders_dict = {}

        for item in all_orders:
            if item.product_id not in orders_dict.keys():
                orders_dict[item.product_id] = item.quantity
            else:
                orders_dict[item.product_id] += item.quantity
        orders_list_sorted = sorted(orders_dict,
                                    key=orders_dict.get, reverse=True)

        bestselling = []
        for i in orders_list_sorted[0:6]:
            bestselling.append(Product.objects.get(id=i))

        context = {
            'categories': categories,
            'products': bestselling,
            'category': 'Bestselling'
        }
        return render(request, 'store/product_list.html', context)


class MostWishedView(WishMixin, View):
    """Returns most wished products."""

    def get(self, request):
        categories = Category.objects.all()
        wishes = Wish.objects.all()

        wishes_dict = {}

        for item in wishes:
            if item.product_id not in wishes_dict.keys():
                wishes_dict[item.product_id] = 1
            else:
                wishes_dict[item.product_id] += 1

        print(wishes_dict)
        wishes_list_sorted = sorted(wishes_dict,
                                    key=wishes_dict.get, reverse=True)
        most_wished = []
        for i in wishes_list_sorted[0:6]:
            most_wished.append(Product.objects.get(id=i))

        context = {
            'categories': categories,
            'products': most_wished,
            'category': 'Most wished'
        }
        return render(request, 'store/product_list.html', context)
