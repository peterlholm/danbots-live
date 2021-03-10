from django.urls import path
from testing import views

urlpatterns = [
    path("test/dummy", views.dummy),
    path("test/template", views.template),
    path("test/pic_info/", views.pic_info, name="pic_info"),
    path("test/show_pic/", views.show_pic, name="show_pic")
]
