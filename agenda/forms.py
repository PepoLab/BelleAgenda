from django import forms

from .models import Appointment, Client, Service


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'client',
            'service',
            'start_at',
            'end_at',
            'notes',
        ]

        widgets = {
            'client': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'service': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'start_at': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                }
            ),
            'end_at': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                }
            ),
        }

    def __init__(self, *args, professional=None, **kwargs):
        super().__init__(*args, **kwargs)

        if professional:
            self.fields['client'].queryset = Client.objects.filter(
                professional=professional,
                active=True
            )

        self.fields['service'].queryset = Service.objects.filter(
            active=True
        )