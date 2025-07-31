from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, TemplateView, CreateView
from .models import Provincia
from django.urls import reverse_lazy
from .forms import ProvinciaForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
    login_url = 'core:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Welcome to the Index Page'
        return context
    

class ProvinciaCreate(LoginRequiredMixin, CreateView):
    model = Provincia
    template_name = 'core/provincia_form.html'
    form_class = ProvinciaForm
    success_url = reverse_lazy('core:provincia_list')
    context_object_name = 'provincia'
    login_url = 'core:login'

    def form_valid(self, form):
        form.instance.provincia = form.cleaned_data['provincia']
        form.instance.pais = form.cleaned_data['pais']
        return super().form_valid(form)


class ProvinciaListView(LoginRequiredMixin, ListView):
    model = Provincia
    template_name = 'provincia_list.html'
    context_object_name = 'provincias'
    login_url = 'core:login'

    def get_queryset(self):
        return Provincia.objects.all().order_by('provincia')