from django.contrib import admin
from django.urls import path, include
from .views import PostCreateView, PostUpdateView, PostDeleteView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('recommend', views.recommend, name='recommend'),
    path('new', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>', views.blogPost, name='blogPost'),
    path('read', views.read, name='read'),
    path('pollute', views.pollute, name='pollute'),
    path('upload', views.upload, name='upload'),
    path('alarm', views.alarm, name='alarm'),
    path('weather', views.weather, name='weather'),
    path('position', views.position, name='position'),

    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

