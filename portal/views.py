from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from shift.models import Project


def is_staff_user(user):
    return user.is_active and user.is_staff


@login_required
@user_passes_test(is_staff_user)
def dashboard(request):
    shift_project_count = Project.objects.count()
    return render(request, 'portal/dashboard.html', {
        'shift_project_count': shift_project_count,
    })
