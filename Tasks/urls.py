from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "Tasks"
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^new-task/$', views.new_task, name='new_task'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<task_type>/', views.tasks, name='tasks'),
    path('task/<task_id>', views.task, name='task'),
    path('task/delete/<task_id>', views.task_delete, name='task_delete'),
    path('notes/', views.notes, name='notes'),
    path('notes/new', views.new_note, name='new_note'),
    path('notes/<note_id>', views.note, name='note'),
    path('manage/', views.task_management, name='task_management'),
    path('temp/', views.temp, name='temp'),
    path('temp_data/', views.temp_data, name='temp_data'),
    path('api/tasks', views.TaskViewSet.as_view({'get': 'list'}), name='api-tasks'),
    path('api/tasks2', views.TaskList.as_view(), name="api-task-list"),
    path('api/tasks2/<pk>', views.TaskDetail.as_view()),

]


urlpatterns = format_suffix_patterns(urlpatterns)


