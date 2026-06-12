from django.contrib import admin
from .models import Project, ShiftType, Staff, Manager, Submission, ShiftSelection

admin.site.register(Project)
admin.site.register(ShiftType)
admin.site.register(Staff)
admin.site.register(Manager)
admin.site.register(Submission)
admin.site.register(ShiftSelection)
