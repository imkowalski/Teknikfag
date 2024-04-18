from picamera import PiCamera, Color
from time import sleep
import datetime

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.awb_mode = "fluorescent"

def take_picture(name=None):
    try:
        time = datetime.datetime.now()
        camera.annotate_foreground = Color('white')
        camera.annotate_background = Color('black')
        camera.annotate_text = str(time.strftime("%d-%m-%Y at %H:%M"))
        camera.annotate_text_size = 50
        camera.awb_mode = "fluorescent"
        camera.start_preview()
        sleep(10)
        if name != None:
            camera.capture('/home/pi/teknikfag/static/img/'+str(name)+'.png')
        else:
            camera.capture('/home/pi/teknikfag/static/img/'+str(time.strftime("%d-%m-%Y.%H"))+'.png')
        camera.stop_preview()
        return str(time.strftime("%d-%m-%Y.%H"))+'.png'
    except e:
        return e
        
