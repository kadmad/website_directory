from django.core.paginator import Paginator, Page
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from crispy_forms.utils import render_crispy_form
from directory.forms import DirectoryForm
from directory.models import Directory
from django.urls import reverse_lazy
import re
from bs4 import BeautifulSoup
from django.conf import settings
import requests
import os
from directory.utils import capture_website_screenshot
import django

class DirectoryListView(ListView):
    model = Directory
    template_name = 'directory/directory_list.html'
    context_object_name = 'directories'
    queryset = Directory.objects.all().order_by("-created_at")   


class TopDirectoryListView(ListView):
    model = Directory
    template_name = 'directory/directory_list.html'
    context_object_name = 'directories'
    queryset = Directory.objects.all().order_by("semrush_rank")   

class DirectoryDetailView(DetailView):
    model = Directory
    template_name = 'directory/directory_detail.html'
    context_object_name = 'directory'

class DirectoryCreateView(CreateView):
    model = Directory
    template_name = 'directory/directory_form.html'
    form_class = DirectoryForm
    success_url = reverse_lazy("website-list")

class DirectoryUpdateView(UpdateView):
    model = Directory
    template_name = 'directory/directory_form.html'
    form_class = DirectoryForm


class DirectoryDeleteView(DeleteView):
    model = Directory
    template_name = 'directory/directory_confirm_delete.html'
    success_url = reverse_lazy('website-list')

