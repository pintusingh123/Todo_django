from django.urls  import path
from tudoapp.views import task_list,task_add,task_deleted ,task_updated ,task_toggle

urlpatterns = [
    path('', task_list , name='task_list'),

    path('add/', task_add , name='task_add'),

    path('edit/<int:pk>/', task_updated , name='task_updated'),

    path('delete/<int:pk>/', task_deleted , name='task_deleted'),

    path('toggle/<int:pk>/', task_toggle , name='task_toggle'),
 
]
