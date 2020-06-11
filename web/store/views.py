from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from cart.forms import CartAddButton, CartAddForm
from store.models import Category, Product, Wish
from store.recommendations import Recommendations


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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


class ProductDetailView(View):
    """Product detail view."""

    r = Recommendations()

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        categories = Category.objects.all()
        form = CartAddForm()
        recommended_products = self.r.suggest_products_for([product], 4)
        print(recommended_products)
        context = {
            'product': product,
            'categories': categories,
            'form': form,
            'recommended_products': recommended_products
        }
        return render(request, 'store/product_detail.html', context)

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
        elif 'del' in request.POST:
            product_id = request.POST.get('del')
            wishes = Wish.objects.filter(product_id=product_id)
            wish = wishes.filter(user_id=user.id)
            wish.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
