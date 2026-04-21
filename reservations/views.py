from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Resource, Booking
from .forms import BookingForm

class ResourceListView(ListView):
    model = Resource
    template_name = 'reservations/resource_list.html'
    context_object_name = 'resources'

class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'reservations/resource_detail.html'
    context_object_name = 'resource'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = BookingForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = BookingForm(request.POST)

        if not request.user.is_authenticated:
            messages.error(request, "Error: Debes iniciar sesión para reservar.")
            return redirect('reservations:resource_detail', pk=self.object.pk)

        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            notes = form.cleaned_data['notes']
            is_recurring = form.cleaned_data.get('is_recurring', False)
            recurrence_weeks = form.cleaned_data.get('recurrence_weeks', 1)

            if not is_recurring:
                recurrence_weeks = 1

            try:
                with transaction.atomic():
                    for i in range(recurrence_weeks):
                        offset = timedelta(days=7 * i)
                        new_booking = Booking(
                            resource=self.object,
                            user=request.user,
                            start_time=start_time + offset,
                            end_time=end_time + offset,
                            notes=notes
                        )
                        new_booking.clean()
                        new_booking.save()

                messages.success(request, f"¡Éxito! Se han registrado {recurrence_weeks} reserva(s) correctamente.")
                return redirect('reservations:resource_detail', pk=self.object.pk)

            except ValidationError as e:
                for msg in e.messages:
                    messages.error(request, f"Error en la semana {i+1}: {msg}")
                return self.render_to_response(self.get_context_data(form=form))
        else:
            messages.error(request, "Por favor, corrige los errores del formulario.")
            return self.render_to_response(self.get_context_data(form=form))
