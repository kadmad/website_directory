from typing import Any
from django.core.paginator import Paginator, Page
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from directory.forms import DirectoryForm
from directory.models import Directory
from django.urls import reverse_lazy
from directory.utils import fetch_live_domain_data, fetch_site_like_data
from django.db.models import Q
from django.contrib import messages
from django.db import transaction

class DirectoryListView(ListView):
    model = Directory
    template_name = 'directory/directory_list.html'
    context_object_name = 'directories'
    queryset = Directory.objects.all().order_by("-created_at")  
    paginator_class = Paginator
    paginate_by = 10  # Number of items to display per page
    def get_queryset(self):
        search = self.request.GET.get("search")
        queryset = super().get_queryset()
        if search:
            queryset = queryset.filter(Q(domain__icontains=search) | Q(title__icontains=search) | Q(description__icontains=search))
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search")
        return context

class TopDirectoryListView(ListView):
    model = Directory
    template_name = 'directory/directory_list.html'
    context_object_name = 'directories'
    queryset = Directory.objects.all().order_by("-worth")   

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            context["worth"] = True
            return context
class DirectoryDetailView(DetailView):
    model = Directory
    template_name = 'directory/directory_detail.html'
    context_object_name = 'directory'
    slug_field = 'slug'  # Specify the slug field to use

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        related_directories = Directory.objects.filter(
            Q(domain__icontains=slug[:3]) | Q(title__icontains=slug[:3]) | Q(description__icontains=slug[:3])
        ).exclude(slug=slug).distinct("id")[:10]
        context["related_directories"] = related_directories
        return context

class DirectoryCreateView(CreateView):
    model = Directory
    template_name = 'directory/directory_form.html'
    form_class = DirectoryForm
    success_url = reverse_lazy("website-list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        with transaction.atomic():
            obj = form.save()
            obj = fetch_site_like_data(obj)
            return super().form_valid(form)     

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Form submission failed. Please check the errors.")
        return super().form_invalid(form)
    
class DirectoryUpdateView(UpdateView):
    model = Directory
    template_name = 'directory/directory_form.html'
    form_class = DirectoryForm


class DirectoryDeleteView(DeleteView):
    model = Directory
    template_name = 'directory/directory_confirm_delete.html'
    success_url = reverse_lazy('website-list')

class RemovalRequestCreateView(CreateView):
    model = Directory
    template_name = 'directory/under_maintenance.html'
    form_class = DirectoryForm
    success_url = reverse_lazy("website-list")

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        return HttpResponse(render(request, 'directory/under_maintenance.html'))
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)     

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)