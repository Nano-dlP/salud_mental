
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView
from .models import Persona
from .forms import PersonaForm
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    template_name = "persona/persona_form.html"
    form_class = PersonaForm
    success_url = reverse_lazy('persona:persona_list')
    context_object_name = 'persona'
    login_url = 'core:login'

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Set the user to the current logged-in user
        return super().form_valid(form)


class PersonaListView(LoginRequiredMixin, CreateView):
    model = Persona
    template_name = "persona/persona_list.html"
    context_object_name = 'personas'
    login_url = 'core:login'
    
    def get_queryset(self):
        return Persona.objects.all().order_by('apellido', 'nombre')
    
        