
from re import template
from django.urls import path
from portal import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('landing/', views.Login.as_view(), name='landing'), 
    path('signup/', views.SignUp.as_view(), name='signup'), 
    path('login/', views.Login.as_view(), name='login'), 
    path('logout/', views.Logout.as_view(), name='logout'), 
    path('dashboard/', views.Home.as_view(), name='home'), 
    path('', views.Home.as_view(), name='home'), 
    path('projects/', views.AddProject.as_view(), name='add_project'), 
    path('my_projects/', views.MyProjectsComment.as_view(), name='my_projects'), 
    path('my_projects/<str:id>/', views.MyProjectsComment.as_view(), name='my_projects'), 
    path('server/status/', views.ToggleServerStatus.as_view(), name='toggle'), 
    path('server/status/<str:id>/', views.ToggleServerStatus.as_view(), name='toggle'), 
    path('project/comments/', views.ProjectsComment.as_view(), name='add_comment'),
    path('add/comment/', views.ProjectsComment.as_view(), name='comments'),
    path('all/comments/', views.ProjectsComment.as_view(), name='all_comments'),
    path('project/comments/<str:id>', views.ProjectsComment.as_view(), name='comments'),
    path('all/comments/<str:id>', views.ProjectsComment.as_view(), name='all_comments'),
    path('view/projects/', views.ViewProjects.as_view(), name='view_project'),
    path('detete/project/', views.AddProject.as_view(), name='delete_project'),
    path('detete/project/<str:id>/', views.AddProject.as_view(), name='delete_project'), 
    path('add/user/toproject/', views.AddUserToProject.as_view(), name='add_user_to_project'),
]
