from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('list-users/', views.UserAPIView.as_view(), name='user_api'),
    path('register/', views.RegisterAPIView.as_view(), name='register_api'),
    path('login/', views.LoginAPIView.as_view(), name='login_api'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout_api'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile_api'),
]