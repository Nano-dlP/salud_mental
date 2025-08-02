from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Institucion
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from .forms import InstitucionForm



class InstitucionCreateView(LoginRequiredMixin, CreateView):
    model = Institucion
    template_name = 'institucion/institucion_form.html'
    form_class = InstitucionForm
    success_url = reverse_lazy('institucion:institucion_list')
    context_object_name = 'institucion'
    login_url = 'core:login'

    def form_valid(self, form):
        form.instance.institucion = form.cleaned_data['institucion']
        form.instance.tipo_institucion = form.cleaned_data['tipo_institucion']
        #form.instance.user_crea = self.request.user
        return super().form_valid(form)


class InstitucionListView(LoginRequiredMixin, ListView):
    model = Institucion
    template_name = 'institucion/institucion_list.html'
    context_object_name = 'instituciones'
    login_url = 'core:login'

    def get_queryset(self):
        return Institucion.objects.all().order_by('institucion')
    

class InstitucionUpdateView(LoginRequiredMixin, UpdateView):
    model = Institucion
    template_name = 'institucion/institucion_form.html'
    form_class = InstitucionForm
    success_url = reverse_lazy('institucion:institucion_list')
    context_object_name = 'institucion'
    login_url = 'core:login'

    def form_valid(self, form):
        form.instance.institucion = form.cleaned_data['institucion']
        form.instance.tipo_institucion = form.cleaned_data['tipo_institucion']
        #form.instance.user_modifica = self.request.user
        return super().form_valid(form)


class InstitucionDetailView(TemplateView):
    template_name = 'institucion/institucion_detail.html'  # Tu template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')  # Obtiene el pk desde la URL
        institucion = get_object_or_404(Institucion, pk=pk)
        context['institucion'] = institucion
        return context