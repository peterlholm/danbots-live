#
# stich a number of images to one image
#
import os
import cv2
import imutils
from imutils import paths

def stitch_files(image_list, outputfile):
    DEBUG=False
    if DEBUG:
        print ("Input:", image_list)
        print("Output:", outputfile)
        #print("OpenCV Version", format(cv2.__version__))
        #print ("is cv3", imutils.is_cv3())
    imagePaths = image_list
    # loop over the image paths, load each one, and add them to our
    # images to stich list
    images = [] 
    for imagePath in imagePaths:
        path = str(imagePath)
        #print(path)
        image = cv2.imread(path)
        if image is not None:
            images.append(image)
            #print(image.shape)
        else:
            print("Billedfejl:", imagePath)

    # initialize OpenCV's image sticher object and then perform the image
    stitcher = cv2.Stitcher_create() # if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)
    if status==0:
        if os.path.exists(outputfile):
            os.remove(outputfile)
        cv2.imwrite(str(outputfile), stitched)
        if DEBUG:
            i=0
            for img in images:
                cv2.imshow("billed"+str(i), img)
                i +=1
            # display the output stitched image to our screen
            cv2.imshow("Stitched", stitched)
            print ("tast")
            cv2.waitKey(0)
        return True
    else:
        print ("Stich mislykket Status:",status)
        return False


if __name__ == "__main__":
    print("Starting")
    files = ['data\\clinics\\1\\stitch\\file1.jpg','data\\clinics\\1\\stitch\\file3.jpg',]
    output ="ud.jpg"
    result = stitch_files(files, output)
    print ("Result:", result)
    image = cv2.imread(output)
    cv2.imshow("Stitched", image)
    print ("tast")
    cv2.waitKey(0)

                #result = stich_files(filelist, file_folder / "ud.jpg")
                #import threading
                # t = threading.Thread(target=long_process,
                #                             args=args,
                #                             kwargs=kwargs)
                # t.setDaemon(True)
                # t.start()
                # return HttpResponse()
                #print("Stiching result", result)
                #return redirect("/test/pic_info/")
