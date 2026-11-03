from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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