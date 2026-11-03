from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .forms import AppointmentForm
from .models import Appointment, Client, Professional, Service


class AppointmentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='profissional',
            password='senha123'
        )

        self.professional = Professional.objects.create(
            user=self.user,
            name='Profissional Teste'
        )

        self.client = Client.objects.create(
            professional=self.professional,
            name='Cliente Teste',
            phone='11999999999'
        )

        self.service = Service.objects.create(
            name='Serviço Teste',
            duration_minutes=60,
            price=100
        )

        self.start_at = timezone.now().replace(
            second=0,
            microsecond=0
        )

    def create_appointment(self, start_at=None, end_at=None):
        start_at = start_at or self.start_at
        end_at = end_at or start_at + timedelta(hours=1)

        return Appointment.objects.create(
            professional=self.professional,
            client=self.client,
            service=self.service,
            start_at=start_at,
            end_at=end_at
        )

    def test_cria_agendamento_valido(self):
        appointment = self.create_appointment()

        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(
            appointment.professional,
            self.professional
        )

    def test_impede_conflito_de_horario(self):
        self.create_appointment()

        conflicting = Appointment(
            professional=self.professional,
            client=self.client,
            service=self.service,
            start_at=self.start_at + timedelta(minutes=30),
            end_at=self.start_at + timedelta(hours=1, minutes=30)
        )

        with self.assertRaises(ValidationError):
            conflicting.save()

    def test_horario_final_deve_ser_posterior_ao_inicio(self):
        appointment = Appointment(
            professional=self.professional,
            client=self.client,
            service=self.service,
            start_at=self.start_at,
            end_at=self.start_at
        )

        with self.assertRaises(ValidationError):
            appointment.save()

    def test_agendamento_cancelado_nao_bloqueia_novo_horario(self):
        appointment = self.create_appointment()
        appointment.status = 'cancelled'
        appointment.save()

        new_appointment = self.create_appointment()

        self.assertEqual(Appointment.objects.count(), 2)


class AppointmentFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='profissional',
            password='senha123'
        )

        self.professional = Professional.objects.create(
            user=self.user,
            name='Profissional Teste'
        )

        self.active_client = Client.objects.create(
            professional=self.professional,
            name='Cliente Ativo',
            phone='11999999999',
            active=True
        )

        self.inactive_client = Client.objects.create(
            professional=self.professional,
            name='Cliente Inativo',
            phone='11888888888',
            active=False
        )

        self.active_service = Service.objects.create(
            name='Serviço Ativo',
            duration_minutes=60,
            price=100,
            active=True
        )

        self.inactive_service = Service.objects.create(
            name='Serviço Inativo',
            duration_minutes=60,
            price=100,
            active=False
        )

    def test_formulario_mostra_apenas_clientes_ativos(self):
        form = AppointmentForm(
            professional=self.professional
        )

        client_ids = list(
            form.fields['client'].queryset.values_list(
                'id',
                flat=True
            )
        )

        self.assertIn(
            self.active_client.id,
            client_ids
        )

        self.assertNotIn(
            self.inactive_client.id,
            client_ids
        )

    def test_formulario_mostra_apenas_servicos_ativos(self):
        form = AppointmentForm(
            professional=self.professional
        )

        service_ids = list(
            form.fields['service'].queryset.values_list(
                'id',
                flat=True
            )
        )

        self.assertIn(
            self.active_service.id,
            service_ids
        )

        self.assertNotIn(
            self.inactive_service.id,
            service_ids
        )