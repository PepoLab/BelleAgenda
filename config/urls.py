from django.contrib import admin
from django.urls import path, include

from agenda.views import agenda_home, appointment_create


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', agenda_home, name='agenda_home'),
    path(
        'agendamentos/novo/',
        appointment_create,
        name='appointment_create'
    ),
]