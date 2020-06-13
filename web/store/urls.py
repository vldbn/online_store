from django.urls import path
from store import views

app_name = 'store'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='productlist'),
    path('category/<str:slug>/', views.ProductCategoryListView.as_view(),
         name='productlist-by-category'),
    path('product/<str:slug>/', views.ProductDetailView.as_view(),
         name='product-detail'),
    path('wishlist/', views.WishListView.as_view(), name='wishlist'),
    path('recommendations/<int:user_id>/', views.RecommendationsView.as_view(),
         name='recommendations')
]
