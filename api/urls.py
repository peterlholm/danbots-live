from django.urls import path
from api import views

urlpatterns = [
    path("api/register", views.register, name="register"),
    path('api/sendpic', views.sendpic, name="sendpic"),
    path('api/test', views.test, name="test"),
]
