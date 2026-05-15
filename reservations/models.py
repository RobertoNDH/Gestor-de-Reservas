from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Resource(models.Model):
    RESOURCE_TYPES = (
        ('court', 'Pista Deportiva'),
        ('room', 'Sala de Reuniones'),
        ('other', 'Otro'),
    )

    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='other', verbose_name="Tipo de Recurso")
    capacity = models.PositiveIntegerField(null=True, blank=True, verbose_name="Capacidad")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"


class Availability(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    )

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='availabilities', verbose_name="Recurso")
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name="Día de la semana")
    start_time = models.TimeField(verbose_name="Hora de inicio")
    end_time = models.TimeField(verbose_name="Hora de finalización")

    def __str__(self):
        return f"{self.resource.name} - {self.get_day_of_week_display()} ({self.start_time} a {self.end_time})"

    class Meta:
        verbose_name = "Disponibilidad"
        verbose_name_plural = "Disponibilidades"
        unique_together = ('resource', 'day_of_week', 'start_time')


class Booking(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings', verbose_name="Recurso")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', verbose_name="Usuario")
    start_time = models.DateTimeField(verbose_name="Inicio de reserva")
    end_time = models.DateTimeField(verbose_name="Fin de reserva")
    notes = models.TextField(blank=True, verbose_name="Notas")
    is_cancelled = models.BooleanField(default=False, verbose_name="Cancelada")

    def __str__(self):
        return f"Reserva de {self.user.username} - {self.resource.name} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
    def clean(self):
        super().clean()
        
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("La fecha de inicio debe ser anterior a la fecha de finalización.")
            
            if not hasattr(self, 'resource_id') or not self.resource_id:
                return
            
            day_of_week = self.start_time.weekday()
            req_start_time = self.start_time.time()
            req_end_time = self.end_time.time()
            
            availabilities = Availability.objects.filter(
                resource=self.resource,
                day_of_week=day_of_week,
                start_time__lte=req_start_time,
                end_time__gte=req_end_time
            )
            
            if not availabilities.exists():
                raise ValidationError("El recurso no está disponible (o está cerrado) en esta franja horaria.")
            
            if not self.is_cancelled:
                overlapping = Booking.objects.filter(
                    resource=self.resource,
                    is_cancelled=False,
                    start_time__lt=self.end_time,
                    end_time__gt=self.start_time
                )
                if self.pk:
                    overlapping = overlapping.exclude(pk=self.pk)
                    
                if overlapping.exists():
                    raise ValidationError("Ya existe una reserva que se solapa con el horario indicado.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['start_time']
