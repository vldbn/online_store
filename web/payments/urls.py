from django.urls import path
from payments import views

app_name = 'payments'
urlpatterns = [
    path('process/', views.PaymentProcessView.as_view(), name='process'),
    path('done/', views.payments_done, name='done'),
    path('canceled/', views.payments_canceled, name='canceled')
]
