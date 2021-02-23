""" Views for the API module """
import os
#from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from common.models import Scanner
from live.settings import CLINIC_PATH #MEDIA_ROOT, 
from lib.stitch_pic import stich_files
from .forms import PicForm

# pylint: disable=old-division

def register(request):
    RESPONSE = {
        #'apiurl': 'http://live.danbots.com/api/',
        'sessionid': '12345'
    }
    deviceid = request.GET.get('deviceid')
    charge = request.GET.get('charge')
    localip = request.GET.get('localip')
    hwmodel = request.GET.get('hwmodel')
    swversion = request.GET.get('swversion')
    remoteip = request.META['REMOTE_ADDR']
    print (timezone.now())
    if deviceid != None:
        try:
            scanner = Scanner.objects.get(Serial=deviceid)
        except Scanner.DoesNotExist:
            # create new record
            scanner = Scanner(Serial=deviceid,Clinic=None, Charge=charge, LastRegister=timezone.now(),RemoteIp=remoteip, LocalIp=localip)
        else:
            scanner.LastRegister = timezone.now()
            scanner.Charge = charge
            scanner.RemoteIp = remoteip
            scanner.LocalIp = localip
        scanner.HWmodel=hwmodel
        scanner.SWversion=swversion    
        scanner.save()
        jresponse = {
            **RESPONSE,
            'clinicname': "peters klinik",
            'clinicno': 27,
            }
    else:
        print('No scanner found')
        jresponse = {
            **RESPONSE,
            'error': 1,
            'errortext': 'Scanner not found'
        }        
    return JsonResponse(jresponse)

def save_uploaded_file(handle, filepath):
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)
    return

@csrf_exempt
def sendpic(request): 
    picform = PicForm()
    mycontext = {
        'pic': picform,
        'name': "Peter",
    }
    clinic=1
    if request.method == 'POST':
        picform = PicForm(request.POST, request.FILES)
        if picform.is_valid():
            FileFolder = CLINIC_PATH / str(clinic)
            if request.POST.get('cmd')=="stitch":
                FileFolder = FileFolder / "stitch"
                os.makedirs(FileFolder, exist_ok=True)

            scannerid = picform.cleaned_data['deviceid']
            print ("ScannerID", scannerid)
            filelist =[]
            if request.FILES.get('Picture'):
                pictures = request.FILES.getlist('Picture')
                for p in pictures:
                    filepath = FileFolder / p.name
                    filelist.append(filepath)
                    save_uploaded_file(p, filepath)
            # for debug
            for p in ['Pic1','Pic2','Pic3']:
                if request.FILES.get(p): 
                    filelist.append(FileFolder / request.FILES[p].name)
                    save_uploaded_file(request.FILES[p], FileFolder / request.FILES[p].name) 
            if request.POST.get('cmd')=="stitch":
                print("Stitching.....")
                result = stich_files(filelist, FileFolder / "ud.jpg")
                #import threading
                # t = threading.Thread(target=long_process,
                #                             args=args,
                #                             kwargs=kwargs)
                # t.setDaemon(True)
                # t.start()
                # return HttpResponse()
                print("Stiching result", result)
            if request.FILES.get('Pic1'):
                # debug
                param = "?"
                for f in request.FILES.items():
                    param += "picture=" +f[1].name + "&"
                param += 'stitch=ud.jpg'
                url = "/test/pic_info/" + param
                #print(url)
                return redirect(url)
            else:
                return JsonResponse({'result':"OK"})
        print ("not valid", picform.errors)
        return render(request, 'api/pic.html', mycontext)
    return render(request, 'api/pic.html', mycontext)

def test(request):
    return HttpResponse("OK")
