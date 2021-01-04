from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='graph_view-home'),
    path('about', views.about, name='graph_view-about'),
    path('visualisation', views.visualisation, name='graph_view-visualisation'),
    path('visualisation2', views.visualisation2,
         name='graph_view-visualisation2'),
    path('avenir', views.avenir, name='graph_view-avenir')
]
