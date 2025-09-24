from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_page, name='root_search_page'),
    path('search/', views.search_page, name='search_page'),
    path('search/results/', views.search_results, name='search_results'),
]
