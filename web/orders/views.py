import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
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
            # TODO uncomment email sending
            order_created.delay(order.id)
            request.session['order_id'] = order.id

            return redirect(reverse('payments:process'))


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


@staff_member_required
def admin_order_detail(request, id):
    """Display order detail view in admin panel."""

    order = get_object_or_404(Order, id=id)
    context = {
        'order': order
    }
    return render(request, 'admin/orders/admin_order_detail.html',
                  context)


@staff_member_required
def admin_order_to_pdf(request, id):
    """Export order to pdf using orders/pdf.html template and
    css styles for it from pdf.css. CSS directory depends on
    debug const in settings.py."""

    if settings.DEBUG:
        css = settings.STATICFILES_DIR + '/css/pdf.css'
    else:
        css = settings.STATIC_ROOT + '/css/pdf.css'

    order = get_object_or_404(Order, id=id)
    context = {
        'order': order
    }
    html = render_to_string('orders/pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[css])

    return response
