#from pathlib import Path
import os
from pathlib import Path
from datetime import datetime
from PIL import Image, ExifTags
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import  login_required  # permission_required,
from django.http import HttpResponse #, HttpResponseForbidden
from common.models import Scanner, Clinic
from live.settings import CLINIC_PATH, CLINIC_URL
from appl.stitch_pic import stitch_files
#from .forms import ScannerForm

CONTEXT = {
            'clinic_name': "",
            'date2': datetime.now()
        }

def init_session_context(request):
    """Init the clinic session variables"""
    if request.session.get('clinic_no') is None:
        #print( "init new session")
        if request.user.is_anonymous:
            clinic_obj = Clinic.objects.get(pk=1)
        else:
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

def public_home(request):
    return render(request, 'public_home.html')

def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('clinic'))
    else:
        return render(request, 'web/home.html', CONTEXT)

def web_help(request):
    return render(request, 'web/help.html', CONTEXT)

@login_required
def clinic_home(request):
    context = init_session_context(request)
    clinic_no= request.session['clinic_no']
    scanners = list(Scanner.objects.filter(Clinic__No=clinic_no).values())
    mycontext = { **context, "scannerlist": scanners}
    return render(request, 'web/clinic.html', mycontext)

@login_required
def scan_pic(request):
    context = init_session_context(request)
    clinic_no= request.session['clinic_no']
    scanners = list(Scanner.objects.filter(Clinic__No=clinic_no).values())
    active_device = request.session.get('active_device')

    if request.method == 'GET':
        active_device = request.GET.get('deviceid')
        if active_device:
            #print ("device", active_device)
            request.session['active_device'] = active_device

    scannerlist=[]
    for s in scanners:
        #print("scanner",s)
        selected=''
        if s['Serial']==active_device:
            selected='selected'
        scannerlist.append({'serial': s['Serial'], 'nameid': s['Name']+'('+s['Serial']+')', 'selected': selected })

    mycontext = {**context,
            'active_device': active_device,
            'scannerlist': scannerlist,
            'power': 50,
            'online': True
    }

    mycontext = {**context,
            'active_device': active_device,
            'scannerlist': scannerlist,
            'power': 50,
            'online': True
    }

    return render(request, 'web/scan_pic.html', mycontext)

@login_required
def scanner_list(request):
    context = init_session_context(request)
    clinic = request.session['clinic_no']
    # clinic = 1
    admin = request.GET.get('admin')
    #print (not admin)
    if not admin:
        scanners = list(Scanner.objects.filter(Clinic_id=clinic).values())
    else:
        scanners = list(Scanner.objects.all().order_by('-LastRegister').values())

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
    if not request.GET.get('deviceid'):
        return HttpResponse("Error")
    context = init_session_context(request)
    deviceid = request.GET.get('deviceid')
    if deviceid:
        scanner = Scanner.objects.get(Serial=deviceid)
    else:
        return HttpResponse("Deviceid Error")
        #return render(request,'web/control.html', context)
    #print(scanner.LocalIp)
    scan_url = "http://"+scanner.LocalIp+":8080"
    mycontext = { **context,
            'scan_url': scan_url,
            'pic_url': "/static/tand.jpg",
            '3d_url': "/static/3d_2.png",
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
            'page_title': "stitch",
            'pic' : pic,
            'folder' : folder,
            'stitch' : stitchurl,
            }
    #print(mycontext)
    return render(request,'web/stitch.html', mycontext)

@login_required
def control(request):
    """ Show the scanning results """
    context = init_session_context(request)
    deviceid = request.GET.get('deviceid')
    if deviceid:
        scanner = Scanner.objects.get(Serial=deviceid)
    else:
        return render(request,'web/control.html', context)
    controlcmd = request.GET.get('control')
    if controlcmd == "2dscan":
        print("2D scan")
    elif controlcmd == "3dscan":
        pass
    else:
        pass

    mycontext = { **context,
        'page_title': "Scanner Control",
        'device': scanner,
        'deviceid': deviceid,
        'state' : "dummy",
        }
    return render(request,'web/control.html', mycontext)

@login_required
def show_picture(request):
    """ Show the scanning results """
    context = init_session_context(request)
    deviceid = request.GET.get('deviceid')

    pic_file = "data/clinics/1/picture/file.jpg"
    img = Image.open(pic_file)
    exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS } # pylint: disable=protected-access

    print(context)
    mycontext = { **context,
        'page_title': "Scanner Control",
        'deviceid': deviceid,
        'picture' : "/data/clinics/1/picture/file.jpg",
        'exif': exif
        }
    #print(mycontext)
    return render(request,'web/show_picture.html', mycontext)

def test(request):
    return HttpResponse("Hello, Django!")
