from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('users/', views.UserAPIView.as_view(), name='users'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('leave-request/',views.LeaveRequestAPIView.as_view(),name='leave-request'),
    path('leaves/',views.LeaveListAPIView.as_view(),name='leaves'),
    path('leaves/<int:pk>/',views.LeaveResponseDetailAPIView.as_view(),name='leave-response'),
    path('overtime-log/',views.OvertimeLogListCreateAPIView.as_view(),name='overtime-log'),
    path('payroll-run/',views.PayrollRunListCreateAPIView.as_view(),name='payroll-run'),
    path('payroll-run/<int:pk>/',views.PayrollRunUpdateAPIView.as_view(),name='update_payroll-run'),
]