from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, get_object_or_404
from cart.cart import Cart
from store.models import Category
from users.forms import UserForm
from orders.forms import OrderProfileForm
from orders.models import Order, OrderItem
from orders.tasks import order_created


class CreateOrderView(LoginRequiredMixin, View):
    """Create order view."""

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user_form = UserForm(instance=user)
        profile_form = OrderProfileForm(instance=user.profile)
        categories = Category.objects.all()
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'categories': categories
        }
        return render(request, 'orders/order_create.html', context)

    def post(self, request):
        cart = Cart(request)
        user = User.objects.get(username=request.user.username)
        user_form = UserForm(request.POST, instance=user)
        profile_form = OrderProfileForm(request.POST, instance=user.profile)
        categories = Category.objects.all()
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            order = Order.objects.create(user=user)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            order_created.delay(order.id)

            context = {
                'order': order,
                'categories': categories
            }
            return render(request, 'orders/order_created.html', context)


class OrderListView(LoginRequiredMixin, View):
    """Order list view."""

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        orders = Order.objects.filter(user=user)
        categories = Category.objects.all()
        context = {
            'orders': orders,
            'categories': categories
        }
        return render(request, 'orders/order_list.html', context)


class OrderDetailView(LoginRequiredMixin, View):
    """Order detail view."""

    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        items = OrderItem.objects.filter(order=order)
        categories = Category.objects.all()
        context = {
            'order': order,
            'categories': categories,
            'items': items
        }
        return render(request, 'orders/order_list_detail.html', context)
