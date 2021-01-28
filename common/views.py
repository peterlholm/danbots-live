from os import makedirs
from pathlib import Path
from django.shortcuts import render
from django.contrib.auth.models import User
from live.settings import CLINIC_PATH
from common.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required

# Create your views here.

def save_uploaded_file(handle, filepath):
    print ('Handle: ', handle)
    print ('Filename', filepath)
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)
    return

#@login_required
@permission_required('common.add_clinic',raise_exception=True)
def clinic(request):
    form=ClinicForm()
    mycontext = {
           'form': form,
    }
    print("her")
    if request.method == 'POST':
        print("most")
        form = ClinicForm(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            newclinic = form.save()
            print(newclinic)
            clinicstr = str(form.cleaned_data['No'])
            clinicfolder = CLINIC_PATH / clinicstr / 'info'
            print(clinicfolder)            
            makedirs(clinicfolder, mode=0o77, exist_ok=True)
            print("11", form.cleaned_data)
            if form.cleaned_data['Logo']:
                filepath = clinicfolder / request.FILES['Logo'].name
                save_uploaded_file(request.FILES['Logo'], filepath)
                print(clinicstr)
            return HttpResponseRedirect('/')
        else:
            print ("ngoet er glat")
    else:
            form=ClinicForm()
    mycontext = {
        'form': form,
        }
    return render(request, 'clinicadm.html', mycontext)

@login_required
def createuser(request):
    createform = UserForm()
    mycontext = {
           'form': createform,
    }

    if request.method == 'POST':
        #print('FILES: ', request.FILES)
        createform = UserForm(request.POST, request.FILES)
        if createform.is_valid():
            user = User.objects.create_user(createform.cleaned_data['Login'], 
                createform.cleaned_data['Email'], createform.cleaned_data['Password'])
            print (user)
            user.first_name = createform.cleaned_data['FirstName']
            user.last_name = createform.cleaned_data['LastName']
            print(user)
            user.save()
            return render(request, 'web/home.html')
        #return render(request, 'createuser.html', mycontext)
    return render(request, 'createuser.html', mycontext)
