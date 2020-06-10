from django.urls import path
from orders import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.CreateOrderView.as_view(), name='create'),
    path('orderlist/', views.OrderListView.as_view(), name='list'),
    path('order/<int:id>/', views.OrderDetailView.as_view(), name='detail'),
    path('admin/order/<int:id>/', views.admin_order_detail,
         name='admin_order_detail'),
    path('admin/order/<int:id>/pdf/', views.admin_order_to_pdf,
         name='admin_order_pdf')
]
