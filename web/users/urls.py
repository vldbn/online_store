from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update/profile', views.ProfileUpdateView.as_view(),
         name='update-profile'),
    path('update/password', views.PasswordUpdateView.as_view(),
         name='update-password'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.logout_view, name='logout')
]
