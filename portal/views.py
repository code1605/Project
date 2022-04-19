from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, View
from portal.models import Project


class Home(ListView):
    template_name = 'base.html'
    model = Project

    def get_context_data(self, **kwargs):
        print(super(Home, self).get_context_data(**kwargs))
        return super(Home, self).get_context_data(**kwargs)
