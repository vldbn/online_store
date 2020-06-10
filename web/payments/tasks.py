import weasyprint
from io import BytesIO
from celery import task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order


@task
def send_pdf(order_id):
    if settings.DEBUG:
        css = settings.STATICFILES_DIR + '/css/pdf.css'
    else:
        css = settings.STATIC_ROOT + '/css/pdf.css'

    order = Order.objects.get(id=order_id)
    user = User.objects.get(id=order.user.id)

    email_host = settings.EMAIL_HOST_USER

    subject = f'Order nr. {order.id}'
    message = f'Deaf {user.first_name} {user.last_name}, ' \
              f'You have successfully made an order. ' \
              f'Your order ID is {order.id}'
    email = EmailMessage(subject, message, email_host, [user.email])

    context = {
        'order': order
    }

    html = render_to_string('orders/pdf.html', context)
    out = BytesIO()
    stylesheets = [weasyprint.CSS(css)]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    mail_send = email.send()
    # mail_send = send_mail(subject, message, email, [user.email])

    return mail_send
