from django.urls import path, include
from django.contrib.auth import urls
from django.contrib.auth import views as auth_views
from common import views

urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("adm/clinic", views.clinic, name="clinicadm"),
    path("adm/createuser", views.createuser, name="createuser"),
]