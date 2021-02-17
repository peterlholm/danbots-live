#import os
from django.shortcuts import render
#from django.http import HttpResponse
from live.settings import  CLINIC_URL # CLINIC_PATH,
from web.views import init_clinic, init_context

# def get_pic_info(file):
#     #import PIL.Image
#     return "exif tekst"

def pic_info(request):
    init_clinic(request)
    context = init_context(request)
    Folder = CLINIC_URL +"1/stitch/"
    pic=[]
    pictures = request.GET.getlist('picture')
    print(pictures)
    if pictures:
        for p in pictures:
            pic.append (Folder+p)
    else:
        for i in range(1,6):
            pic.append(Folder+"file"+str(i)+".jpg")

    print(pic)
    # for p in pictures:
    #     pic.append(CLINIC_URL +"1/stitch/" + p)
    stitchurl = Folder + request.GET.get('stitch',"ud.jpg")
    mycontext = { **context,
            'pic' : pic,
            'stitch' : stitchurl,
            }
    return render(request,'test/pic_info.html', mycontext) 
