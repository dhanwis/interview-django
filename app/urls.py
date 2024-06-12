
from django.urls import path
from .views import LoginView, VerifyOTPView,UserRegistration

urlpatterns=[
    path("register/", UserRegistration.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]