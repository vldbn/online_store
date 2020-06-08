from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Category, Product
from cart.cart import Cart
from cart.forms import CartAddForm, CartAddButton


class CartView(LoginRequiredMixin, View):
    """Cart detail view."""

    def get(self, request):
        cart = Cart(request)
        categories = Category.objects.all()
        for item in cart:
            item['update_quantity_form'] = CartAddForm(
                initial={'quantity': item['quantity'],
                         'update': True})
        context = {
            'cart': cart,
            'categories': categories
        }
        return render(request, 'cart/cart_detail.html', context)


@require_POST
@login_required
def cart_add(request, product_id):
    """Add item into a cart."""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data.get('quantity')
        update_quantity = form.cleaned_data.get('update')
        cart.add(product=product, quantity=quantity,
                 update_quantity=update_quantity)
        return redirect('cart:detail')


@require_POST
@login_required
def cart_add_quick(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddButton(request.POST)
    previous_page = request.META['HTTP_REFERER']
    if form.is_valid():
        quantity = form.quantity
        update_quantity = form.cleaned_data.get('update')
        cart.add(product=product, quantity=quantity,
                 update_quantity=update_quantity)

        return redirect(previous_page)


@login_required
def cart_remove(request, product_id):
    """Remove item from a cart."""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')
