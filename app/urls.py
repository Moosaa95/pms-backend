from django.urls import path 
from .endpoints import *

urlpatterns = [
    path("projects", ProjectListCreateAPIView.as_view(), name="projects"),
    path("tasks", TaskListCreateAPIView.as_view(), name="tasks"),
    path("filter", ProjectFilter.as_view(), name="filter"),
    
    
]