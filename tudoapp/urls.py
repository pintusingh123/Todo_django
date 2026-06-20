from django.urls  import path
from tudoapp.views import task_list,task_add,task_deleted ,task_updated ,task_toggle ,login_view,signup_view,logout_view

urlpatterns = [
    path('', task_list , name='task_list'),

    path('add/', task_add , name='task_add'),

    path('edit/<int:pk>/', task_updated , name='task_updated'),

    path('delete/<int:pk>/', task_deleted , name='task_deleted'),

    path('toggle/<int:pk>/', task_toggle , name='task_toggle'),
    path("signup", signup_view, name="signup_view" ),

    path("login",login_view, name="login_view"),
    path("logout",logout_view, name="logout_view")
 
]
