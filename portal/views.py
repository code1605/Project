
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from services.sentiment import Sentiment
# Create your views here.
from django.views.generic import ListView, View
from portal.serializers import CommentSerializer, ProjectSerializer
from portal.models import Project, Comment
from users.models import Users
from django.db.models import Sum
from django.contrib.auth import views as auth_views
from django.contrib.auth import (
    login,
    logout,
    authenticate
)
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(LoginRequiredMixin, ListView):
    template_name = 'base.html'
    login_url = settings.LOGIN_URL
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_members'] = Users.objects.all()
        projects = Project.objects.all()
        context['projects_score'] = round(projects.aggregate(Sum('project_progress')).get('project_progress__sum')/projects.count(), 2) if projects else 0
        return context

class AddProject(LoginRequiredMixin, View):
    template_name = 'base.html'  
    model = Project

    def post(self, request, *args, **kwargs):
        context = {'object_list': Project.objects.all()}
        context['company_members'] = Users.objects.all()
        print(request.POST)
        serializer = ProjectSerializer(data=request.POST)
        if serializer.is_valid():
            Project.create(serializer.validated_data)
            return redirect('home')
        context['errors'] = serializer.errors
        print(context)
        return redirect('home')
    
    #add get method
    def get(self, request, *args, **kwargs):
        self.model.objects.filter(id=kwargs['id']).delete()
        return redirect('home')


class ViewProjects(LoginRequiredMixin, View):
    template_name = 'projects.html'
    model = Project

    def get(self, request, *args, **kwargs):
        context = {'object_list': Project.objects.all()}
        context['company_members'] = Users.objects.all()
        return render(request, self.template_name, context=context)


class ProjectsComment(LoginRequiredMixin, View):
    template_name = 'comments.html'
    model = Comment

    def get(self, request, *args, **kwargs):
        context = {
            'project': Project.objects.filter(id=kwargs['id']).first(), 
            'comments': self.model.objects.filter(project__id=kwargs.get("id"))
        }
        print(context)
        return render(request, self.template_name, context=context)


    def post(self, request, *args, **kwargs):
        print(request.POST)
        serializer = CommentSerializer(data=request.POST)
        if serializer.is_valid():
            print(serializer.validated_data)
            project = Project.objects.filter(id=serializer.validated_data.get('project_id')).first()
            project.add_comment(request.user, serializer.validated_data.get('comment'), sentiment=-1)
            return redirect('comments', id=serializer.validated_data.get('project_id'))
        context = {}
        context['errors'] = serializer.errors
        print(context)
        return redirect('comments', id=serializer.validated_data.get('project_id'))


class MyProjectsComment(LoginRequiredMixin, View):
    template_name = 'my_projects.html'
    model = Comment

    def get(self, request, *args, **kwargs):
        if kwargs.get('id'):
            project = Project.objects.filter(id=kwargs.get('id')).first()
        else:
            project = Project.objects.filter(project_team__in=[request.user]).first()


        context = {
            'project':   project , 
            'projects': Project.objects.filter(project_team__in=[request.user]),
            'comments': self.model.objects.filter(project__id=kwargs.get("id"))
        }
        print(context)
        return render(request, self.template_name, context=context)


    def post(self, request, *args, **kwargs):
        print(request.POST)
        serializer = CommentSerializer(data=request.POST)
        if serializer.is_valid():
            print(serializer.validated_data)
            project = Project.objects.filter(id=serializer.validated_data.get('project_id')).first()
            sentiment =  Sentiment(settings.MODEL, serializer.validated_data.get('comment'))
            print("SENTIMENT : ", sentiment)
            project.add_comment(request.user, serializer.validated_data.get('comment'), sentiment)
            return redirect('my_projects', id=serializer.validated_data.get('project_id'))
        context = {}
        context['errors'] = serializer.errors
        print(context)
        return redirect('my_projects', id=serializer.validated_data.get('project_id'))


class Login(auth_views.LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        print("""Security check complete. Log the user in.""")
        user = form.get_user()
        login(self.request, user)
        if user.is_superuser:
            return redirect('home')
        return redirect('my_projects')

    def form_invalid(self, form):
        print("IN FORM_INVALID")
        messages.error(self.request, "Incorrect Credentials!", extra_tags="login_error")
        return self.render_to_response(self.get_context_data(form=form, context={}))

class Logout(auth_views.LogoutView):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        print("IN LOGOUT")
        return redirect('login')


class ToggleServerStatus(LoginRequiredMixin, View):
    template_name = 'comments.html'
    model = Project


    def get(self, request, *args, **kwargs):
        project = self.model.objects.filter(id=kwargs.get('id')).first()
        if project:
            project.update_status()
        return redirect('view_project')


class AddUserToProject(LoginRequiredMixin, View):
    template_name = 'comments.html'
    model = Project 


    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data.get('project_team'))
        project = self.model.objects.filter(id=data.get('project_id')).first()
        user = Users.objects.filter(id=data.get('project_team')).first()
        print(project,  user)
        if project and user:
            project.add_user(user)
        return redirect('view_project')


class SignUp(View):
    template_name = 'signup.html'
    model = Users 


    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context=context)
