from blog.views import CategoryPostsView, TagPostsView, handler404
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.views.defaults import page_not_found

# my_blog/urls.py
from django.conf.urls import handler404

handler404 = 'blog.views.handler404'  
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('post_list/', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_details, name='post_detail'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
