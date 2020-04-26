from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('about', views.about, name='About'),
    path('contact', views.contact, name='Contact'),
    path('search', views.search, name='Search'),
    path('signup', views.handleSignup, name='HandleSignup'),
    path('login', views.handleLogin, name='HandleLogin'),
    path('logout', views.handleLogout, name='HandleLogout'),
]
