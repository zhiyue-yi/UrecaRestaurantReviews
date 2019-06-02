from django.urls import path
from . import views

# route management for web application
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('loc/<int:diningarea_id>', views.loc, name='loc'),

    # to be shifted to another application
    path('api/toprated', views.toprated, name='toprated'),
    path('api/diningarea/<int:id>', views.diningarea, name='diningarea'),
    path('api/menu', views.menu, name='menu'),
    path('api/comment', views.comment, name='comment'),
    path('api/feedback', views.feedback, name='feedback'), # comment without csrf
    path('api/query', views.query, name='search'),
    path('api/query/<str:keyword>', views.query, name='search'),
]