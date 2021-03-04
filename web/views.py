#from pathlib import Path
import os
from pathlib import Path
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import  login_required  # permission_required,
from django.http import HttpResponse #, HttpResponseForbidden
from common.models import Scanner, Clinic
from live.settings import CLINIC_PATH, CLINIC_URL
from lib.stitch_pic import stitch_files

# Create your views here.


CONTEXT = {
            'clinic_name': "",
            'date': datetime.now()
        }

# def init_clinic1(request):
#     """Init the clinic session variables"""
#     if request.session.get('clinic_no') is None:
#         print ("Putting in clinic 1")

#         request.session['clinic_no'] = 1
#         request.session['clinicname'] = "klinik navn"
#     else:
#         request.session['clinic_no'] = 1
#         request.session['clinicname'] = "klinik admin"

#         # init clinic
#         # try:
#         #     clinic_no = request.user.user2clinic.clinic
#         # except ObjectDoesNotExist:
#         #     print ('Not a registeret user')
#         #     clinic_no=1
#         # clinic_name = Clinic.objects.get(clinic_no=clinic_no).ClinicName
#         # request.session['clinic_no'] = clinic_no
#         # request.session['clinic_name'] = clinic_name
#         # print('init_clinic', clinic_name)
#     #print ("clinic_no", request.session.get('clinic_no'))
#     return True

# def init_context1(request):
#     """Init the context directory"""
#     context = {
#         **CONTEXT,
#         'clinic_name': "",
#         'date': datetime.now()
#     }
#     return context

def init_session_context(request):
    """Init the clinic session variables"""
    if request.session.get('clinic_no') is None:
        #print( "init new session")
        try:
            clinic_obj = request.user.user2clinic.clinic
        except ObjectDoesNotExist:
            #print ('Not a registeret user')
            clinic_obj = Clinic.objects.get(pk=1)
        request.session['clinic_no'] = clinic_obj.No
        request.session['clinic_name'] = clinic_obj.Name
        request.session['clinic_path'] = str(CLINIC_PATH / str(clinic_obj.No))
    context = {
        **CONTEXT,
        'clinic_no': request.session['clinic_no'],
        'clinic_name': request.session['clinic_name'],
        'date': datetime.now()
    }
    return context

def home(request):
    """
    Display the users home page
    **Context**
    **Template:**
    :template:`web/home.html`
    """
    #context = init_session_context(request)
    # context = {
    #             'date': datetime.now()
    # }
    return render(request, 'web/home.html', CONTEXT)

def web_help(request):
    return render(request, 'web/help.html', CONTEXT)

@login_required
def clinic_home(request):
    context = init_session_context(request)
#    if not init_clinic(request):
#        return HttpResponseForbidden()
#    context = init_context(request)
    clinic_no= request.session['clinic_no']
    scanners = list(Scanner.objects.filter(Clinic__No=clinic_no).values())
    mycontext = { **context, "scannerlist": scanners}
    return render(request, 'web/clinic.html', mycontext)

@login_required
def scanner_list(request):
    """
    Display list of the users scanners

    **Context**

    ``context``
      et eller andet

    **Template:**

    :template:`web/scannerlist.html`
    """

    context = init_session_context(request)

    # context = init_context(request)
    # ok = init_clinic(request)
    clinic = request.session['clinic_no']
    # clinic = 1
    admin = request.GET.get('admin')
    #print (not admin)
    if not admin:
        scanners = list(Scanner.objects.filter(Clinic_id=clinic).values())
    else:
        scanners = list(Scanner.objects.all().values())

    #print(clinic)
    mycontext = { **context, "scannerlist": [{'device':"1ddd", 'name':"nr1", 'charge':60}, {'device':"3ddd", 'charge':10} ]}
    #scanners = list(Scanner.objects.all().values())
    #print(scanners)

    #print (scanners.values())
    mycontext = { **mycontext, "scannerlist": scanners}
    #print(mycontext)


    return render(request, 'web/scannerlist.html', mycontext)

@login_required
def select_scan(request):
    context = init_session_context(request)

    # init_clinic(request)
    # context = init_context(request)
    clinic_no= request.session['clinic_no']
    scanners = list(Scanner.objects.filter(Clinic__No=clinic_no).values())
    print(scanners)
    print(len(scanners))
    if len(scanners)==0:
        print("vi er er")
        return redirect(reverse('scannerlist'))
    if len(scanners)==1:
        return redirect(reverse('scan')+"?scanner="+scanners[0]['Serial'])
    mycontext = { **context, "scannerlist": scanners}
    return render(request,'web/selectscan.html', mycontext)

@login_required
def scan(request):
    if not request.GET.get('scanner'):
        return HttpResponse("Error")
    context = init_session_context(request)

    #init_clinic(request)
    #context = init_context(request)
    #tmycontext = init_context(request)
    mycontext = { **context,
            'pic1_url': CLINIC_URL + '1/file1.jpg',
            'pic2_url': CLINIC_URL + '1/file2.jpg',
            #'pic1_url': DEVICE_URL,
        }
    print (mycontext)
    return render(request,'web/scan.html', mycontext)

@login_required
def results(request):
    """ Show the scanning results """
    context = init_session_context(request)

    #init_clinic(request)
    #context = init_context(request)

    #print (mycontext)
    return render(request,'web/results.html', context)

@login_required
def stitch(request):
    """ Show the stitch results """
    context = init_session_context(request)
    clinic_no = request.session['clinic_no']
    clinic_path = Path(request.session['clinic_path'])
    filefolder = clinic_path / "stitch"
    url = CLINIC_URL + str(clinic_no) + "/stitch/"
    pic=[]
    folder=[]
    pathlist =[]
    for file in os.listdir(filefolder):
        if os.path.isfile(filefolder / file):
            print(file)
            if file != "stitch.jpg":
                pic.append(url + file)
                pathlist.append(filefolder / file)
        else:
            folder.append(file)
    folder.sort()
    pic.sort()

    if request.GET.get('restitch', None):
        print ("Restitch")
        outpath = filefolder / "stitch.jpg"
        stitch_files(pathlist, outpath  )

    stitchurl = url + "stitch.jpg"
    mycontext = { **context,
            'pic' : pic,
            'folder' : folder,
            'stitch' : stitchurl,
            }
    print(mycontext)
    return render(request,'web/stitch.html', mycontext)


def test(request):
    return HttpResponse("Hello, Django!")
