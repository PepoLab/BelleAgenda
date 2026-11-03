from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .forms import AppointmentForm, ClientForm, ServiceForm
from .models import Appointment, Client, Service


@login_required
def agenda_home(request):
    professional = request.user.professional

    appointments = Appointment.objects.filter(
        professional=professional
    ).exclude(
        status='cancelled'
    ).order_by(
        'start_at'
    )

    context = {
        'appointments': appointments,
    }

    return render(
        request,
        'agenda/home.html',
        context
    )


@login_required
def client_list(request):
    professional = request.user.professional

    clients = Client.objects.filter(
        professional=professional
    ).order_by(
        'name'
    )

    context = {
        'clients': clients,
    }

    return render(
        request,
        'agenda/client_list.html',
        context
    )



@login_required
def client_create(request):
    professional = request.user.professional

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.professional = professional
            client.save()

            return redirect('client_list')

    else:
        form = ClientForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'agenda/client_form.html',
        context
    )




@login_required
def client_edit(request, client_id):
    professional = request.user.professional

    client = Client.objects.get(
        id=client_id,
        professional=professional
    )

    if request.method == 'POST':
        form = ClientForm(
            request.POST,
            instance=client
        )

        if form.is_valid():
            form.save()

            return redirect('client_list')

    else:
        form = ClientForm(
            instance=client
        )

    context = {
        'form': form,
        'client': client,
    }

    return render(
        request,
        'agenda/client_form.html',
        context
    )


@login_required
def client_deactivate(request, client_id):
    professional = request.user.professional

    client = Client.objects.get(
        id=client_id,
        professional=professional
    )

    if request.method == 'POST':
        client.active = False
        client.save()

        return redirect('client_list')

    context = {
        'client': client,
    }

    return render(
        request,
        'agenda/client_deactivate.html',
        context
    )


@login_required
def client_activate(request, client_id):
    professional = request.user.professional

    client = Client.objects.get(
        id=client_id,
        professional=professional
    )

    if request.method == 'POST':
        client.active = True
        client.save()

        return redirect('client_list')

    context = {
        'client': client,
    }

    return render(
        request,
        'agenda/client_activate.html',
        context
    )


@login_required
def appointment_create(request):
    professional = request.user.professional

    if request.method == 'POST':
        form = AppointmentForm(
            request.POST,
            professional=professional
        )

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.professional = professional

            if appointment.client.professional != professional:
                form.add_error(
                    'client',
                    'O cliente selecionado não pertence ao profissional atual.'
                )
            else:
                try:
                    appointment.save()
                except ValidationError as error:
                    form.add_error(None, error)
                else:
                    return redirect('agenda_home')

    else:
        form = AppointmentForm(
            professional=professional
        )

    context = {
        'form': form,
    }

    return render(
        request,
        'agenda/appointment_form.html',
        context
    )
@login_required
def service_list(request):
    services = Service.objects.all().order_by('name')

    context = {
        'services': services,
    }

    return render(
        request,
        'agenda/service_list.html',
        context
    )

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('service_list')

    else:
        form = ServiceForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'agenda/service_form.html',
        context
    )

@login_required
def service_edit(request, service_id):
    service = Service.objects.get(
        id=service_id
    )

    if request.method == 'POST':
        form = ServiceForm(
            request.POST,
            instance=service
        )

        if form.is_valid():
            form.save()

            return redirect('service_list')

    else:
        form = ServiceForm(
            instance=service
        )

    context = {
        'form': form,
        'service': service,
    }

    return render(
        request,
        'agenda/service_form.html',
        context
    )
@login_required
def service_deactivate(request, service_id):
    service = Service.objects.get(
        id=service_id
    )

    if request.method == 'POST':
        service.active = False
        service.save()

        return redirect('service_list')

    context = {
        'service': service,
    }

    return render(
        request,
        'agenda/service_deactivate.html',
        context
    )
@login_required
def service_activate(request, service_id):
    service = Service.objects.get(
        id=service_id
    )

    if request.method == 'POST':
        service.active = True
        service.save()

        return redirect('service_list')

    context = {
        'service': service,
    }

    return render(
        request,
        'agenda/service_activate.html',
        context
    )
@login_required
def appointment_cancel(request, appointment_id):
    professional = request.user.professional

    appointment = Appointment.objects.get(
        id=appointment_id,
        professional=professional
    )

    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()

        return redirect('agenda_home')

    context = {
        'appointment': appointment,
    }

    return render(
        request,
        'agenda/appointment_cancel.html',
        context
    )