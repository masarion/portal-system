from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path('', lambda r: redirect('portal:dashboard', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('portal/', include('portal.urls', namespace='portal')),
    path('shift/', include('shift.urls', namespace='shift')),
]
