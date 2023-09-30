from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index,name=''),
    path('login', views.login),
    path('signup', views.signup),
    path('contact',views.contact),
    path('about',views.about),
    path('index',views.index)
]

