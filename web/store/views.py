from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.shortcuts import render, get_object_or_404
from store.models import Category, Product


class ProductListView(View):
    """Productlist view."""

    def get(self, request):
        # TODO make pagination
        product_list = Product.objects.all()
        paginator = Paginator(product_list, 6)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        categories = Category.objects.all()
        context = {
            'products': products,
            'categories': categories,
            'category': 'All categories'
        }
        return render(request, 'store/product_list.html', context)


class ProductCategoryListView(View):
    """Product list view by category."""

    def get(self, request, slug):
        # TODO make pagination
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
        categories = Category.objects.all()
        context = {
            'products': products,
            'categories': categories,
            'category': category
        }
        return render(request, 'store/product_list.html', context)


class ProductDetailView(View):
    """Product detail view."""

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        categories = Category.objects.all()
        context = {
            'product': product,
            'categories': categories
        }
        return render(request, 'store/product_detail.html', context)
