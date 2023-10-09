from django.urls import path
from . import views

urlpatterns = [
    path('', views.showIndexPage, name="index"),
    path('login/', views.showSigninPage, name="login"),
    path('signup/', views.showSignupPage, name="signup"),
# # 
    path('check_user_exists/', views.check_user_exists, name='check_user_exists'), 
# #    
    path('password_reset_request/', views.password_reset_request, name="password_reset_request"),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('reset_password/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
] 