from django.urls import path
from web import views

urlpatterns = [
    path("", views.home, name="home"),
    path("clinic/", views.clinic_home, name="clinic"),
    path("selectscan/", views.select_scan, name="selectscan"),
    path("scan/", views.scan, name="scan"),
    path("stitch/", views.stitch, name="stitch"),
    path("results/", views.results, name="results"),
    path("scannerlist/", views.scanner_list, name="scannerlist"),
    path("help/", views.web_help)
]
