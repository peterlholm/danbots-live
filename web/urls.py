from django.urls import path
from web import views

urlpatterns = [
    path("public", views.public_home, name="public_home"),
    path("", views.home, name="home"),
    path("clinic/", views.clinic_home, name="clinic"),
    path("scan_pic/", views.scan_pic, name="scan_pic"),
     path("selectscan/", views.select_scan, name="selectscan"),
    path("scan/", views.scan, name="scan"),
    path("stitch/", views.stitch, name="stitch"),
    path("results/", views.results, name="results"),
    path("show_picture/", views.show_picture, name="show_picture"),
    path("scannerlist/", views.scanner_list, name="scannerlist"),
    path("control/", views.control, name="control"),
    path("help/", views.web_help)
]
