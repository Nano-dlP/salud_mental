from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Internacion
from .forms import InternacionForm
# Create your views here.
class InternacionCreateView(LoginRequiredMixin, CreateView):
    model = Internacion
    form_class = InternacionForm
    template_name = 'internacion/internacion_form.html'
    success_url = reverse_lazy('internacion:internacion_list')
    context_object_name = 'internaciones'
    login_url = 'core:login'
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class InternacionListView(LoginRequiredMixin, ListView):
    model = Internacion
    template_name = 'internacion/internacion_list.html'
    context_object_name = 'internaciones'
    login_url = 'core:login'
    
    def get_queryset(self):
        return Internacion.objects.all().order_by('-fecha_internacion')