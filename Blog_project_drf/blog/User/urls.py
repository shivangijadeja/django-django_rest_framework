from django.contrib import admin
from django.urls import path,include
from .views import UserApi,LoginApi, LogoutApi, UserDetails, ChangePassword

urlpatterns = [
    path('user/',UserApi.as_view()),
    path('login/',LoginApi.as_view()),
    path('verify_otp/',LoginApi.as_view()),
    path('logout/',LogoutApi.as_view()),
    path('profile-details/',UserDetails.as_view()),
    path('change-password/',ChangePassword.as_view())
]