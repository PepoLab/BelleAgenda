from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from agenda.models import Appointment, Client, Professional, Service


class Command(BaseCommand):
    help = "Cria os dados de demonstraÃ§Ã£o do BelleAgenda."

    def handle(self, *args, **options):
        username = "avaliador"
        email = "avaliador@belleagenda.com"
        password = "BelleAgenda2026!"

        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": "Avaliador",
            },
        )

        if user_created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS("UsuÃ¡rio avaliador criado.")
            )
        else:
            self.stdout.write(
                self.style.WARNING("UsuÃ¡rio avaliador jÃ¡ existe.")
            )

        professional, professional_created = Professional.objects.get_or_create(
            user=user,
            defaults={
                "name": "Belle Studio",
                "phone": "(11) 99999-9999",
                "specialty": "EstÃ©tica e Beleza",
                "active": True,
            },
        )

        if professional_created:
            self.stdout.write(
                self.style.SUCCESS("Profissional de demonstraÃ§Ã£o criado.")
            )
        else:
            self.stdout.write(
                self.style.WARNING("Profissional de demonstraÃ§Ã£o jÃ¡ existe.")
            )

        services_data = [
            {
                "name": "Corte Feminino",
                "description": "Corte e finalizaÃ§Ã£o.",
                "duration_minutes": 60,
                "price": 80.00,
            },
            {
                "name": "Escova",
                "description": "Escova e finalizaÃ§Ã£o.",
                "duration_minutes": 45,
                "price": 50.00,
            },
            {
                "name": "Manicure",
                "description": "Manicure tradicional.",
                "duration_minutes": 45,
                "price": 40.00,
            },
        ]

        services = {}

        for data in services_data:
            service, _ = Service.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "duration_minutes": data["duration_minutes"],
                    "price": data["price"],
                    "active": True,
                },
            )
            services[data["name"]] = service

        clients_data = [
            {
                "name": "Ana Souza",
                "phone": "(11) 98888-1111",
                "email": "ana.souza@example.com",
                "notes": "Prefere atendimento no perÃ­odo da manhÃ£.",
            },
            {
                "name": "Carolina Oliveira",
                "phone": "(11) 97777-2222",
                "email": "carolina.oliveira@example.com",
                "notes": "Cliente recorrente.",
            },
            {
                "name": "Mariana Santos",
                "phone": "(11) 96666-3333",
                "email": "mariana.santos@example.com",
                "notes": "Primeiro atendimento.",
            },
        ]

        clients = {}

        for data in clients_data:
            client, _ = Client.objects.get_or_create(
                professional=professional,
                name=data["name"],
                defaults={
                    "phone": data["phone"],
                    "email": data["email"],
                    "notes": data["notes"],
                    "active": True,
                },
            )
            clients[data["name"]] = client

        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        appointments_data = [
            {
                "client": clients["Ana Souza"],
                "service": services["Corte Feminino"],
                "start": timezone.make_aware(
                    timezone.datetime.combine(
                        today,
                        timezone.datetime.min.time().replace(hour=10),
                    )
                ),
                "duration": 60,
                "status": "confirmed",
                "notes": "Cliente confirmou pelo WhatsApp.",
            },
            {
                "client": clients["Carolina Oliveira"],
                "service": services["Manicure"],
                "start": timezone.make_aware(
                    timezone.datetime.combine(
                        today,
                        timezone.datetime.min.time().replace(hour=14),
                    )
                ),
                "duration": 45,
                "status": "scheduled",
                "notes": "",
            },
            {
                "client": clients["Mariana Santos"],
                "service": services["Escova"],
                "start": timezone.make_aware(
                    timezone.datetime.combine(
                        tomorrow,
                        timezone.datetime.min.time().replace(hour=9),
                    )
                ),
                "duration": 45,
                "status": "scheduled",
                "notes": "Primeiro atendimento.",
            },
        ]

        for data in appointments_data:
            end = data["start"] + timedelta(minutes=data["duration"])

            Appointment.objects.get_or_create(
                professional=professional,
                client=data["client"],
                service=data["service"],
                start_at=data["start"],
                defaults={
                    "end_at": end,
                    "status": data["status"],
                    "notes": data["notes"],
                },
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Dados de demonstraÃ§Ã£o do BelleAgenda configurados com sucesso!"
            )
        )
        self.stdout.write("UsuÃ¡rio: avaliador")
        self.stdout.write("Senha: BelleAgenda2026!")
