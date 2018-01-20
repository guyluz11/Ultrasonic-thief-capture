from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import glob


def start_record_video(f_camera):
    f_camera.hflip = True
    date1 = time.strftime('%Y-%m-%d %H:%M:%s', time.gmtime())
    print(date1)
    f_camera.start_recording('/home/pi/Videos/Dor video/%s.h264' % date1)
    print('Start record video')


def stop_record_video(f_camera):
    f_camera.stop_recording()
    print('Stop record video')


def get_distance():  # return the distance from the ultra sonic sensor
    time.sleep(1.016)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO):  # GPIO.input(ECHO) == 0
        pass
    start = time.time()

    while GPIO.input(ECHO):  # GPIO.input(ECHO) == 1
        pass
    stop = time.time()
    distance = (stop - start) * 17000
    
    print('The distance is ' + distance)
    return distance


GPIO.setmode(GPIO.BOARD)

TRIG = 36   # Start the measuring from the sonic sensor
ECHO = 38   # The distance from the sonic sensor
camera = PiCamera()
camera_on = False

GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, 0)

GPIO.setup(ECHO, GPIO.IN)

time.sleep(0.1)

dorDistance = get_distance()

videosFolderPath = '/home/' + os.environ["USER"] + '/Videos/*'    # Get the computer user name and save the path of the videos folder
statvfs = os.statvfs('/')

try:
    while True:
        distance1 = get_distance()
        freeSpace = (statvfs.f_frsize * statvfs.f_bavail / 1000000000)  # Free space on the system in gigabytes

        if freeSpace < 5:  # if space on the system is smaller than 5 gb, delete the oldest file
            print("no space")

            while freeSpace < 7:
                list_of_files = glob.glob(videosFolderPath)  # * means all if need specific format then *.csv
                latest_file = min(list_of_files, key=os.path.getctime)
                print(latest_file + " delete oldest file")
                os.remove(videosFolderPath)


        else:
            print("you may proceed")
            if distance1 >= dorDistance + 5 or distance1 <= dorDistance - 5:
                if not camera_on:
                    camera_on = True
                    print('camera on')
                    start_record_video(camera)

            elif dorDistance - 5 < distance1 < dorDistance + 5:
                if camera_on:
                    camera_on = False
                    print('camera off')
                    stop_record_video(camera)
except:
    print("error, no oldest file file found, don't have space to save new video")
    
finally:
    GPIO.cleanup()
