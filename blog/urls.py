from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('post_list/', views.post_list, name='post_list'),
    path('post_detail/<int:id>/', views.post_detail, name='post_detail'),
    path('ticket/', views.ticket, name='ticket'),
    path('post_detail/<int:post_id>/comment',
         views.commnet_post, name='comment_post'),
    path('create-post/', views.createpost, name='create-post'),
    path('search-post/', views.search_post, name='search-post'),
]
