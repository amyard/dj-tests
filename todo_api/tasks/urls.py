from django.urls import path

from tasks import views
from tasks.views import (ProjectListView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView,)


app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='base_view'),
    path('project-create/', ProjectCreateView.as_view(), name='project_create'),
    path('project-update/<str:slug>/', ProjectUpdateView.as_view(), name='project_update'),
    path('project-delete/<str:slug>', ProjectDeleteView.as_view(), name='project_delete'),
    path('project-list/', ProjectListView.as_view(), name='project_list'),
]