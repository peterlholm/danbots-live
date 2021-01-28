from django.contrib import admin

# Register your models here.

from .models import *

class User2clinicAdmin(admin.ModelAdmin):
    #fields = ['ClinicNo', 'ClinicName']
    list_display = ('user', 'clinic')
admin.site.register(User2clinic, User2clinicAdmin)

class ClinicAdmin(admin.ModelAdmin):
    #fields = ['ClinicNo', 'ClinicName']
    list_display = ('No', 'Name', 'Logo')
admin.site.register(Clinic, ClinicAdmin)

class ScannerAdmin(admin.ModelAdmin):
    #fields = ('Serial', 'Clinic', 'Name', 'LastRegister','Charge', 'LocalIp', 'RemoteIp', 'HWmodel','SWversion')
    list_display = ('Serial', 'Clinic', 'LastRegister','Charge')
admin.site.register(Scanner, ScannerAdmin)

# class PatientAdmin(admin.ModelAdmin):
#     list_display = ('PatientNo', 'Name')
# admin.site.register(Patient, PatientAdmin)

# admin.site.register(Picture)
