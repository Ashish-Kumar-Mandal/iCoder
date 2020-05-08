from django.urls import path
from blog import views

urlpatterns = [
    # API to a post comment
    path('postComment', views.postComment, name='PostComment'),

    path('', views.index, name='Index'),
    path('<str:slug>', views.blogPost, name='Post'),    
]
