#from pathlib import Path
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required, login_required
from common.models import Scanner
from live.settings import CLINIC_PATH, CLINIC_URL

# Create your views here.

from django.http import HttpResponse, HttpResponseForbidden

CONTEXT = {
            'clinic_name': "",
        }

def init_clinic(request):
    """Init the clinic session variables"""
    if request.session.get('clinicno') == None:
        print ("not init")

        request.session['clinicno'] = 1
        request.session['clinicname'] = "klinik navn"
    else:
        request.session['clinicno'] = 1
        request.session['clinicname'] = "klinik admin"

        # init clinic
        # try:
        #     clinicno = request.user.user2clinic.clinic
        # except ObjectDoesNotExist:
        #     print ('Not a registeret user')
        #     clinicno=1
        # clinic_name = Clinic.objects.get(ClinicNo=clinicno).ClinicName
        # request.session['clinicno'] = clinicno
        # request.session['clinic_name'] = clinic_name
        # print('init_clinic', clinic_name)
    #print ("clinicno", request.session.get('clinicno'))
    return True

def init_context(request):
    """Init the context directory"""
    context = { 
        **CONTEXT,
        'clinic_name': "",
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
    print(init_context(request))
    return render(request, 'web/home.html', init_context(request))

def help(request):
    return render(request, 'web/help.html', init_context(request))

@login_required
def clinic_home(request):
    if not init_clinic(request):
        return HttpResponseForbidden()
    context = init_context(request)
    clinicno= request.session['clinicno']
    scanners = list(Scanner.objects.filter(Clinic__No=clinicno).values())
    mycontext = { **context, "scannerlist": scanners}
    return render(request, 'web/clinic.html', mycontext)

def scanner_list(request):
    """
    Display list of the users scanners

    **Context**
    
    ``context``
      et eller andet

    **Template:**

    :template:`web/scannerlist.html`
    """
    context = init_context(request)
    ok = init_clinic(request)
    clinic = request.session['clinicno']
    clinic = 1
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

def select_scan(request):
    init_clinic(request)
    context = init_context(request)
    clinicno= request.session['clinicno']
    scanners = list(Scanner.objects.filter(Clinic__No=clinicno).values())
    print(scanners)
    print(len(scanners))
    if len(scanners)==0:
        print("vi er er")
        return redirect(reverse('scannerlist'))
    if len(scanners)==1:
        return redirect(reverse('scan')+"?scanner="+scanners[0]['Serial'])
    mycontext = { **context, "scannerlist": scanners}
    return render(request,'web/selectscan.html', mycontext) 

def scan(request):
    if not request.GET.get('scanner'):
        return HttpResponse("Error")
    init_clinic(request)
    context = init_context(request)
    tmycontext = init_context(request)
    mycontext = { **tmycontext,
            'pic1_url': CLINIC_URL + '1/file1.jpg',
            'pic2_url': CLINIC_URL + '1/file2.jpg',
            #'pic1_url': DEVICE_URL,
        }
    print (mycontext)
    return render(request,'web/scan.html', mycontext) 

def get_pic_info(file):
    import PIL.Image

    return "exif tekst"

def pic_info(request):
    # if not request.GET.get('scanner'):
    #     return HttpResponse("Error - missing scanner")
    init_clinic(request)
    context = init_context(request)
    tmycontext = init_context(request)

    pictures = request.GET.getlist('picture')
    pic=[]
    for p in pictures:
        pic.append(CLINIC_URL +"1/" + p)
    stitch = CLINIC_URL + "1/" + request.GET.get('stitch')
     
    exif = get_pic_info("1/file1.jpg")
    mycontext = { **tmycontext,
            'pic' : pic,
            'stitch' : stitch,
            'pic1_url': CLINIC_URL + '1/file1.jpg',
            'pic2_url': CLINIC_URL + '1/file2.jpg',
            'info' : exif
            #'pic1_url': DEVICE_URL,
        }
    print (mycontext)
    return render(request,'web/pic_info.html', mycontext) 


def results(request):
    """ Show the scanning results """
    init_clinic(request)
    context = init_context(request)
 
    #print (mycontext)
    return render(request,'web/results.html', context) 
   

def test(request):
    return HttpResponse("Hello, Django!")
