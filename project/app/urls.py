from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('login', views.login,name='login'),
    path('signup', views.user_signup,name='signup'),
    path('logout/', views.user_logout, name='logout')
    # path('contact',views.contact, name='contact'),
    # path('about',views.about),
    # path('index',views.index),
    # path('inside',views.inside),
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

