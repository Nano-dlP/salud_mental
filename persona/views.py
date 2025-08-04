
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView, ListView, UpdateView, TemplateView
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


class PersonaListView(LoginRequiredMixin, ListView):
    model = Persona
    template_name = "persona/persona_list.html"
    context_object_name = 'personas'
    login_url = 'core:login'
    
    def get_queryset(self):
        return Persona.objects.all().order_by('apellido', 'nombre')
    

class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    template_name = 'persona/persona_form.html'
    form_class = PersonaForm
    success_url = reverse_lazy('persona:persona_list')
    context_object_name = 'personas'
    login_url = 'core:login'

    def form_valid(self, form):
        form.instance.persona = form.cleaned_data['persona']
        form.instance.tipo_persona = form.cleaned_data['tipo_persona']
        #form.instance.user_modifica = self.request.user
        return super().form_valid(form)


class PersonaDetailView(TemplateView):
    template_name = 'persona/persona_detail.html'  # Tu template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')  # Obtiene el pk desde la URL
        persona = get_object_or_404(Persona, pk=pk)
        context['persona'] = persona
        return context
    

        