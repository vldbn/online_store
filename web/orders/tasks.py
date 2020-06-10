from celery import task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from web.settings import EMAIL_HOST_USER
from orders.models import Order

email = EMAIL_HOST_USER


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    user = User.objects.get(id=order.user.id)
    subject = f'Order nr. {order.id}'
    message = f'Deaf {user.first_name} {user.last_name}, ' \
              f'You have successfully made an order. ' \
              f'Your order ID is {order.id}'
    mail_send = send_mail(subject, message, email, [user.email])

    return mail_send
