from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Institucion
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from django.urls import reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

from .forms import InstitucionForm



class InstitucionCreateView(LoginRequiredMixin, CreateView):
    model = Institucion
    template_name = 'institucion/institucion_form.html'
    form_class = InstitucionForm
    success_url = reverse_lazy('institucion:institucion_list')
    context_object_name = 'institucion'
    login_url = 'core:login'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)

        next_url = self.request.GET.get('next')
        if next_url:
            query_string = urlencode({'institucion_id': self.object.pk})
            return HttpResponseRedirect(f'{next_url}?{query_string}')
        return response


class InstitucionListView(LoginRequiredMixin, ListView):
    model = Institucion
    template_name = 'institucion/institucion_list.html'
    context_object_name = 'instituciones'
    login_url = 'core:login'

    def get_queryset(self):
        return Institucion.objects.all().order_by('institucion')
    
    #Con esta función restrinjo la visualizasión solo a los que tienen estado true
    def get_queryset(self):
        return Institucion.objects.filter(estado=True)
    

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


class InstitucionDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'institucion/institucion_detail.html'  # Tu template
    login_url = 'core:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')  # Obtiene el pk desde la URL
        institucion = get_object_or_404(Institucion, pk=pk)
        context['institucion'] = institucion
        return context
    

def institucion_desactivar(request, pk):
    institucion = get_object_or_404(Institucion, pk=pk)

    if request.method == 'POST':
        institucion.estado=False
        institucion.save()
        messages.success(request, f"{institucion} fue desactivada exitosamente")

    return redirect('institucion:institucion_list')