from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = "Tasks"
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^new-task/$', views.new_task, name='new_task'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<task_type>/', views.tasks, name='tasks'),
    path('task/<task_id>', views.task, name='task'),
    path('manage', views.task_management, name='task_management'),


]