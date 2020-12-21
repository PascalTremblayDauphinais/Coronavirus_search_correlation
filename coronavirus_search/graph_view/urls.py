from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='graph_view-home'),
]
