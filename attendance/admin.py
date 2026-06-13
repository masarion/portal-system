from django.contrib import admin
from .models import Workplace, Employee, AttendanceRecord

admin.site.register(Workplace)
admin.site.register(Employee)
admin.site.register(AttendanceRecord)
