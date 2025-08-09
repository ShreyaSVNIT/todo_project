from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view


'''
urls is responsible for mapping the web addresses to the view functions respectively
syntax: path(the url to put, view page, name shown in template )
'''

urlpatterns = [
    path('', views.signup_view, name='home'),
    path('tasks/', views.task_list, name='task_list'),

    #shows a form (GET) saves a task (POST)
    path('add/', views.add_task, name='add_task'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('mark_completed/<int:pk>/', views.mark_completed, name='mark_completed'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='todo_app/login.html'), name='login'),
    # above line only allows POST, not GET request which is an issue for logout.
    path('logout/', logout_view, name='logout'),
]
