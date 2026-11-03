from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Professional(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='professional'
    )
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    specialty = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='clients'
    )
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Agendado'),
        ('confirmed', 'Confirmado'),
        ('completed', 'Realizado'),
        ('cancelled', 'Cancelado'),
    ]

    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='appointments'
    )

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_at and self.end_at:
            if self.end_at <= self.start_at:
                raise ValidationError(
                    'O horário de término deve ser posterior ao horário de início.'
                )

        if self.professional_id and self.start_at and self.end_at:
            conflicting_appointments = Appointment.objects.filter(
                professional_id=self.professional_id,
                start_at__lt=self.end_at,
                end_at__gt=self.start_at,
            ).exclude(
                status='cancelled'
            )

            if self.pk:
                conflicting_appointments = conflicting_appointments.exclude(
                    pk=self.pk
                )

            if conflicting_appointments.exists():
                raise ValidationError(
                    'O profissional já possui um agendamento neste intervalo de horário.'
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.client.name} - {self.start_at}'