from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .forms import AppointmentForm
from .models import Appointment


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