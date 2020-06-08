from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartView.as_view(), name='detail'),
    path('add/<int:product_id>/', views.cart_add, name='add'),
    path('add-quick/<int:product_id>/', views.cart_add_quick,
         name='add-quick'),
    path('remove/<int:product_id>/', views.cart_remove, name='remove')
]
