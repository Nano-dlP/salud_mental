from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Profesional
from .forms import ProfesionalForm


class ProfesionalCreateView(CreateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = "profesional/profesional_create.html"
    success_url = reverse_lazy("profesional:profesional_list")  # redirige al listado después de guardar


class ProfesionalListView(ListView):
    model = Profesional
    template_name = "profesional/profesional_list.html"
    context_object_name = "profesionales"
    queryset = Profesional.objects.all().order_by('user__first_name', 'user__last_name')
    
    
class ProfesionalUpdateView(UpdateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = "profesional/profesional_create.html"
    success_url = reverse_lazy("profesional:profesional_list")

class ProfesionalDeleteView(DeleteView):
    model = Profesional
    template_name = "profesional_confirm_delete.html"
    # The line `success_url = reverse_lazy("profesionalprofesional_list")` in the
    # `ProfesionalDeleteView` class is setting the URL to redirect to after successfully deleting a
    # `Profesional` object. However, there seems to be a typo in the URL name. It should be
    # `success_url = reverse_lazy("profesional:profesional_list")` instead of `success_url =
    # reverse_lazy("profesionalprofesional_list")`.
    success_url = reverse_lazy("profesional:profesional_list")    