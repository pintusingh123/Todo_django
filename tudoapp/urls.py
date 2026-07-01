from django.urls import path

from tudoapp.views import (
    task_list,
    task_add,
    task_deleted,
    task_updated,
    task_toggle,
    restore_task,
    delete_forever,
    login_view,
    signup_view,
    logout_view,
    trash_view,

    # Password Reset Views
    forgot_password,
    reset_password,
)

urlpatterns = [

    # ==========================
    # Todo URLs
    # ==========================
    path('', task_list, name='task_list'),

    path('add/', task_add, name='task_add'),

    path('edit/<int:pk>/', task_updated, name='task_updated'),

    path('delete/<int:pk>/', task_deleted, name='task_deleted'),

    path('trash/', trash_view, name='trash_view'),
    path("restore/<int:pk>/", restore_task, name="restore_task"),
    path("delete-forever/<int:pk>/", delete_forever, name="delete_forever"),

    path('toggle/<int:pk>/', task_toggle, name='task_toggle'),

    # ==========================
    # Authentication
    # ==========================
    path("signup", signup_view, name="signup_view"),

    path("login", login_view, name="login_view"),

    path("logout", logout_view, name="logout_view"),

    # ==========================
    # Custom Password Reset
    # ==========================
    path(
        "forgot-password/",
        forgot_password,
        name="forgot_password",
    ),

    path(
        "reset-password/<str:token>/",
        reset_password,
        name="reset_password",
    ),

]