from django.urls import path
from test import views

urlpatterns = [
    #path("test", views.home, name="home"),
    path("test/pic_info/", views.pic_info, name="pic_info")
]