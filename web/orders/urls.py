from django.urls import path
from orders import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.CreateOrderView.as_view(), name='create'),
    path('orderlist/', views.OrderListView.as_view(), name='list'),
    path('order/<int:id>/', views.OrderDetailView.as_view(), name='detail')
]