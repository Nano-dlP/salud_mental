from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, CreateView
from .models import Expediente
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages


from .forms import ExpedienteForm




class ExpedienteListView(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'expediente/expediente_list.html'
    context_object_name = 'expedientes'
    login_url = 'core:login'

    def get_queryset(self):
        return Expediente.objects.all().order_by('identificador')
    



class ExpedienteCreateView(LoginRequiredMixin, CreateView):
    model = Expediente
    template_name = "expediente/expediente_form.html"
    form_class = ExpedienteForm
    success_url = reverse_lazy('expediente:expediente_list')
    context_object_name = 'expediente'
    login_url = 'core:login'

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Set the user to the current logged-in user
        return super().form_valid(form)

