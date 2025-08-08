from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, TemplateView, CreateView
from .models import Provincia
from persona.models import Persona
from django.urls import reverse_lazy
from .forms import ProvinciaForm

from django.contrib.auth.decorators import login_required
from .forms import SesionInicialForm

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
    



@login_required
def sesion_inicial(request):
    if request.method == 'POST':
        form = SesionInicialForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha'].strftime('%d/%m/%Y')
            localidad = form.cleaned_data['localidad']  # instancia Localidad

            # Guardamos en sesión los datos clave
            request.session['fecha_sesion'] = fecha
            request.session['localidad_sesion'] = localidad.id
            request.session['localidad_nombre'] = localidad.localidad  # nombre para mostrar

            return redirect('core:dashboard')  # tu vista principal
    else:
        form = SesionInicialForm()

    return render(request, 'core/sesion_inicial.html', {'form': form})

@login_required
def dashboard(request):
    fecha = request.session.get('fecha_sesion')
    localidad_id = request.session.get('localidad_sesion')

    # Por ejemplo, filtrar pacientes por localidad seleccionada
    personas = Persona.objects.filter(localidad_id=localidad_id)

    return render(request, 'core/dashboard.html', {
        'fecha': fecha,
        'personas': personas,
    })