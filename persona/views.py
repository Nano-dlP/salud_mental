

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from .models import Persona
from .forms import PersonaForm
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404


from django.http import JsonResponse
from django.views.decorators.http import require_GET

from dal import autocomplete



class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    template_name = "persona/persona_form.html"
    form_class = PersonaForm
    success_url = reverse_lazy('persona:persona_list')
    context_object_name = 'persona'
    login_url = 'core:login'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)

        next_url = self.request.GET.get('next')
        if next_url:
            query_string = urlencode({'persona_id': self.object.pk})
            return HttpResponseRedirect(f'{next_url}?{query_string}')
        return response



class PersonaListView(LoginRequiredMixin, ListView):
    model = Persona
    template_name = "persona/persona_list.html"
    context_object_name = 'personas'
    login_url = 'core:login'
    
    def get_queryset(self):
        return Persona.objects.all().order_by('apellido', 'nombre')
    


class BusquedaAvanzadaListView(LoginRequiredMixin, ListView):
    model = Persona
    template_name = "persona/busqueda_avanzada.html"
    context_object_name = 'personas'
    login_url = 'core:login'
    
    def get_queryset(self):
        return Persona.objects.busqueda_fecha()
    



class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    template_name = 'persona/persona_form.html'
    form_class = PersonaForm
    success_url = reverse_lazy('persona:persona_list')
    context_object_name = 'personas'
    login_url = 'core:login'

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente.")
        return super().form_valid(form)



class PersonaDetailView(TemplateView):
    template_name = 'persona/persona_detail.html'  # Tu template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')  # Obtiene el pk desde la URL
        persona = get_object_or_404(Persona, pk=pk)
        context['persona'] = persona
        return context
    


class PersonaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # filtrar según lo que escribe el usuario
        
        if not self.request.user.is_authenticated:
            return Persona.objects.none()

        qs = Persona.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q) | qs.filter(apellido__icontains=self.q)

        return qs
    




@require_GET
def buscar_personas(request):
    q = request.GET.get("q", "").strip()
    personas = Persona.objects.filter(
        apellido__icontains=q
    ) | Persona.objects.filter(
        nombre__icontains=q
    ) | Persona.objects.filter(
        numero_documento__icontains=q
    )

    personas = personas.distinct()[:20]

    data = [
        {"id": p.id, "nombre": p.nombre, "apellido": p.apellido, "dni": p.numero_documento}
        for p in personas
    ]
    return JsonResponse(data, safe=False)