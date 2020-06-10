from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from payments.tasks import send_pdf


class PaymentProcessView(LoginRequiredMixin, View):
    """Payment processing view."""

    gateway = settings.BRAINTREE_GATEWAY

    def get(self, request):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        client_token = self.gateway.client_token.generate()
        context = {
            'order': order,
            'client_token': client_token
        }
        return render(request, 'payments/payments_process.html', context)

    def post(self, request):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        nonce = request.POST.get('payment_method_nonce')
        result = self.gateway.transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            send_pdf.delay(order_id)
            return redirect('payments:done')
        else:
            return redirect('payments:canceled')


@login_required
def payments_done(request):
    return render(request, 'payments/payments_done.html')


@login_required
def payments_canceled(request):
    return render(request, 'payments/payments_canceled.html')
