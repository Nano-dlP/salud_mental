from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, TemplateView
from .models import Provincia


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Welcome to the Index Page'
        return context
    

class ProvinciaListView(ListView):
    model = Provincia
    template_name = 'provincia_list.html'
    context_object_name = 'provincias'

    def get_queryset(self):
        return Provincia.objects.all().order_by('provincia')