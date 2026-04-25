from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.dateparse import parse_datetime
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
        if self.request.user.is_authenticated:
            context['user_bookings'] = Booking.objects.filter(
                resource=self.object,
                user=self.request.user,
                is_cancelled=False,
                end_time__gte=timezone.now()
            ).order_by('start_time')
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

def api_resource_bookings(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    bookings = Booking.objects.filter(resource=resource, is_cancelled=False)
    
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')
    
    if start_str:
        start_dt = parse_datetime(start_str)
        if start_dt:
            bookings = bookings.filter(end_time__gte=start_dt)
            
    if end_str:
        end_dt = parse_datetime(end_str)
        if end_dt:
            bookings = bookings.filter(start_time__lte=end_dt)
            
    
    events = []
    for booking in bookings:
        events.append({
            'title': 'Reservado',
            'start': booking.start_time.isoformat(),
            'end': booking.end_time.isoformat(),
            'color': '#ff4757',
            'textColor': '#ffffff',
            'display': 'block'
        })
    
    return JsonResponse(events, safe=False)

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.is_cancelled = True
        booking.save()
        messages.success(request, f"Notificación: Tu reserva para el {booking.start_time.strftime('%d/%m/%Y %H:%M')} ha sido cancelada satisfactoriamente.")
        return redirect('reservations:resource_detail', pk=booking.resource.pk)
    return redirect('reservations:resource_list')
