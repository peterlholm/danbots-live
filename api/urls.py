from django.urls import path
from api import views

urlpatterns = [
    path("api/register", views.register, name="register"),
    path('api/sendpic', views.pic, name="pic"),
    path('api/test', views.test, name="test"),

    # path("clinic/", views.clinic_home, name="clinic"),
    # path("help/", views.help)
]