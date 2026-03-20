from django.core.paginator import Paginator, Page
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from crispy_forms.utils import render_crispy_form
from directory.forms import DirectoryForm, CommentForm
from directory.models import Directory, Comment
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

class DirectoryDetailView(View):
    def get(self, request, pk):
        directory = get_object_or_404(Directory, pk=pk)
        comments = directory.comments.all()
        form = CommentForm()
        return render(request, 'directory/directory_detail.html', {
            'directory': directory, 'comments': comments, 'form': form
        })

    def post(self, request, pk):
        directory = get_object_or_404(Directory, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.directory = directory
            comment.save()
            return redirect('website-detail', pk=pk)
        comments = directory.comments.all()
        return render(request, 'directory/directory_detail.html', {
            'directory': directory, 'comments': comments, 'form': form
        })

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

