from django.contrib.auth.views import LogoutView
from django.urls import path

from base.views.site import (CustomLoginView, RegisterPage, TaskCreate,
                             TaskDelete, TaskDetail, TaskList, TaskReorder,
                             TaskUpdate)

from base.views.api import todo_api_list, todo_api_detail

urlpatterns = [
    # Site
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),

    # API
    path('api/', todo_api_list, name='todo_api_list'),
    path('api/<int:pk>/', todo_api_detail, name='todo_api_detail'),
]
