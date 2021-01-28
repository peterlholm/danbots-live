from datetime import datetime
from django.shortcuts import render, redirect
from live.settings import MEDIA_ROOT, CLINIC_PATH
from lib.stitch_pic import stich_files

# Create your views here.

#import os 
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from scan_project.models import Scanner

# Create your views here.
from django.http import HttpResponse, JsonResponse
from .forms import PicForm
# from web.config import APP_NAME
from common.models import Scanner
# from scan_project.settings import MEDIA_ROOT


def register(request):
    RESPONSE = {
        'apiurl': 'http://live.danbots.com/api/',
        'sessionid': '12345'
    }
    
    deviceid = request.GET.get('deviceid')
    charge = request.GET.get('charge')
    localip = request.GET.get('localip')
    hwmodel = request.GET.get('hwmodel')
    swversion = request.GET.get('swversion')
    remoteip = request.META['REMOTE_ADDR']
    print("DeviceID", deviceid)
    print("charge", charge)
    if deviceid != None:
        try:
            scanner = Scanner.objects.get(Serial=deviceid)
            pass
        except Scanner.DoesNotExist:
            # create new record
            scanner = Scanner(Serial=deviceid,Clinic=None, Charge=charge, LastRegister=datetime.now(),RemoteIp=remoteip, LocalIp=localip)
            #scanner.save()
            #Charge=charge
        else:
            scanner.LastRegister = datetime.now()
            scanner.Charge = charge
            scanner.RemoteIp = remoteip
            scanner.LocalIp = localip
        scanner.HWmodel=hwmodel
        scanner.SWversion=swversion    
        scanner.save()

        # print(scanner)
        # print(scanner.Clinic)
        # print(scanner.Clinic.ClinicName)
        # jresponse = {
        #     **RESPONSE,
        #     'clinicname': scanner.Clinic.ClinicName,
        #     'clinicno': scanner.Clinic.ClinicNo,
        #     }
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

# def find_scanner_clinic(scannerid):
#     print('Scannerid:',scannerid)
#     return 1

def save_uploaded_file(handle, filepath):
    #print ('Handle: ', handle)
    #print ('Filename', filepath)
    with open(filepath, 'wb+') as destination:
        for chunk in handle.chunks():
            destination.write(chunk)
    return

@csrf_exempt
def pic(request): 
    picform = PicForm()
    mycontext = {
        'pic': picform,
        'name': "Peter",
    }
    clinic=1
    if request.method == 'POST':
        print('FILES: ', request.FILES)
        print('POST', request.POST)
        picform = PicForm(request.POST, request.FILES)
        if picform.is_valid():
            FileFolder = CLINIC_PATH / str(clinic)
            scannerid = picform.cleaned_data['scannerid']
            #print ("ScannerID", scannerid)
            #clinic = find_scanner_clinic(scannerid)
            #print(request.POST.get('Pic1'))
            if request.FILES.get('Picture'):
                pictures = request.FILES.getlist('Picture')
                print("type", type(pictures))
                print ('Picture', pictures)
                for p in pictures:
                    print(p)
                    filepath = FileFolder / p.name
                    print (filepath)
                    save_uploaded_file(p, filepath)
            for p in ['Pic1','Pic2','Pic3']:
                if request.FILES.get(p): 
                    save_uploaded_file(request.FILES[p], FileFolder /request.FILES[p].name) 
            if request.POST.get('cmd')=="stitch":
                print("Stitching.....")
                files =[]
                for f in request.FILES.items():
                    #print(f[1].name)
                    files.append(FileFolder / f[1].name)
                #print(type(files[0]))
                result = stich_files(files, FileFolder / "ud.jpg")
                import threading

                # t = threading.Thread(target=long_process,
                #                             args=args,
                #                             kwargs=kwargs)
                # t.setDaemon(True)
                # t.start()
                # return HttpResponse()
                print("Stiching result", result)
            param = "?"
            for f in request.FILES.items():
                param += "picture=" +f[1].name + "&"
            param += 'stitch=ud.jpg'
            url = "/pic_info/" + param
            print(url)
            return redirect(url)
            return JsonResponse({'result':"OK"})
        print ("not valid", picform.errors)
        return render(request, 'api/pic.html', mycontext)
    return render(request, 'api/pic.html', mycontext)

def test(request):
    return HttpResponse("OK")
