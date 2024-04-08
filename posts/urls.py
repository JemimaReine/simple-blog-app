from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.create_post, name='create_post'),
    path('post/<str:id>', views.post, name='post'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
     path('contact/', views.contact, name='contact'),
      path('post/<int:post_id>/like_dislike/', views.like_dislike_post, name='like_dislike_post'),
       path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
]