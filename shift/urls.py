from django.urls import path
from . import views

app_name = 'shift'

urlpatterns = [
    # 管理者
    path('', views.project_list, name='project_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:pk>/dashboard/', views.submission_dashboard, name='submission_dashboard'),
    path('projects/<int:pk>/schedule/', views.submission_schedule, name='submission_schedule'),
    path('projects/<int:pk>/export/', views.export_excel, name='export_excel'),

    # スタッフ提出（ログイン不要）
    path('submit/<uuid:token>/', views.staff_submit, name='staff_submit'),
    path('submit/<uuid:token>/save/', views.staff_submit_save, name='staff_submit_save'),
]
