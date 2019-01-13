from django.urls import path
from . import views

# route management for web application
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('loc', views.loc, name='loc'),
]