import os
from os.path import isfile
from django.shortcuts import render
#from django.http import HttpResponse
from django.contrib.auth.decorators import  login_required  # permission_required,
from live.settings import  CLINIC_URL, CLINIC_PATH
from web.views import init_session_context #init_clinic, init_context

# def get_pic_info(file):
#     #import PIL.Image
#     return "exif tekst"

@login_required
def pic_info(request):
    #init_clinic(request)
    #context = init_context(request)
    context = init_session_context(request)

    folder = CLINIC_URL +"1/stitch/"
    pic=[]
    pictures = request.GET.getlist('picture')
    print(pictures)
    if pictures:
        for pic in pictures:
            pic.append (folder+pic)
    else:
        for i in range(1,6):
            pic.append(folder+"file"+str(i)+".jpg")

    print(pic)
    # for p in pictures:
    #     pic.append(CLINIC_URL +"1/stitch/" + p)
    stitchurl = folder + request.GET.get('stitch',"ud.jpg")
    mycontext = { **context,
            'pic' : pic,
            'stitch' : stitchurl,
            }
    return render(request,'test/pic_info.html', mycontext)

@login_required
def show_pic(request):
    context = init_session_context(request)
    clinic_no = request.session['clinic_no']
    #init_clinic(request)
    #context = init_context(request)
    pic_folder = CLINIC_URL +"1/stitch/"
    print(CLINIC_PATH, type(CLINIC_PATH))
    filefolder = CLINIC_PATH / str(clinic_no)
    folder = request.GET.get('folder', '')
    if folder:
        filefolder = filefolder / folder
    url = CLINIC_URL + str(clinic_no) + "/" + folder + "/"
    print (filefolder, type(filefolder))
    print (url)
    pic=[]
    folder=[]
    for file in os.listdir(filefolder):
        if isfile(filefolder / file):
            pic.append(url + file)
        else:
            folder.append(file)
    folder.sort()
    pic.sort()
    #pictures = request.GET.getlist('picture')
    #print(pictures)
    # if pictures:
    #     for p in pictures:
    #         pic.append (Folder+p)
    # else:
    #     for i in range(1,6):
    #         pic.append(Folder+"file"+str(i)+".jpg")

    print(pic)
    # for p in pictures:
    #     pic.append(CLINIC_URL +"1/stitch/" + p)
    stitchurl = folder + request.GET.get('stitch',"ud.jpg")
    mycontext = { **context,
            'pic' : pic,
            'folder' : folder,
            'stitch' : stitchurl,
            }
    return render(request,'test/show_pic.html', mycontext)
