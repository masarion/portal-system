from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # QRスキャン（認証不要）
    path('scan/<uuid:token>/',        views.scan_show,  name='scan_show'),
    path('scan/<uuid:token>/stamp/',  views.scan_store, name='scan_store'),

    # 管理
    path('management/',                          views.dashboard,        name='dashboard'),
    path('management/records/',                  views.attendance_list,  name='attendance_list'),
    path('management/records/export/',           views.attendance_export,name='attendance_export'),
    path('management/employees/',                views.employee_list,    name='employee_list'),
    path('management/employees/import/',         views.employee_import,  name='employee_import'),
    path('management/employees/new/',            views.employee_form,    name='employee_create'),
    path('management/employees/<int:pk>/edit/',  views.employee_form,    name='employee_edit'),
    path('management/employees/<int:pk>/delete/',views.employee_delete,  name='employee_delete'),
    path('management/employees/<int:pk>/qr/',    views.employee_qr,      name='employee_qr'),
    path('management/workplaces/',               views.workplace_list,   name='workplace_list'),
    path('management/workplaces/new/',           views.workplace_form,   name='workplace_create'),
    path('management/workplaces/<int:pk>/edit/', views.workplace_form,   name='workplace_edit'),
    path('management/workplaces/<int:pk>/delete/',views.workplace_delete,name='workplace_delete'),
]
