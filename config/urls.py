from django.contrib import admin
from django.urls import path, include

from agenda.views import (
    agenda_home,
    appointment_create,
    client_list,
    client_create,
    client_edit,
    client_deactivate,
    client_activate,
    service_list,
    service_create,
    service_edit,
    service_deactivate,
    service_activate,
    appointment_cancel,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path(
        '',
        agenda_home,
        name='agenda_home'
    ),

    path(
        'agendamentos/novo/',
        appointment_create,
        name='appointment_create'
    ),

    path(
        'clientes/',
        client_list,
        name='client_list'
    ),

    path(
        'clientes/novo/',
        client_create,
        name='client_create'
    ),
     path(
    'clientes/<int:client_id>/editar/',
    client_edit,
    name='client_edit'
),
    path(
    'clientes/<int:client_id>/desativar/',
    client_deactivate,
    name='client_deactivate'
),
    path(
    'clientes/<int:client_id>/ativar/',
    client_activate,
    name='client_activate'
),
path(
    'servicos/',
    service_list,
    name='service_list'
),
path(
    'servicos/novo/',
    service_create,
    name='service_create'
),
path(
    'servicos/<int:service_id>/editar/',
    service_edit,
    name='service_edit'
),
path(
    'servicos/<int:service_id>/desativar/',
    service_deactivate,
    name='service_deactivate'
),
path(
    'servicos/<int:service_id>/ativar/',
    service_activate,
    name='service_activate'
),
path(
    'agendamentos/<int:appointment_id>/cancelar/',
    appointment_cancel,
    name='appointment_cancel'
),
]