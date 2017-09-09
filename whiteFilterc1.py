
import sys
from time import sleep
import numpy as np
import cv2

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse

import motion
import time
import almath
import math
from math import exp,pow,fabs,cos,sin,sqrt

nao_ip="0.0.0.0"


# Global variable to store the ReactToTouch module instance
####--------------------- Global variables, all proxies and Nao resources
class globalVariables:

    def __init__(self, robotIP):
        self.IP = robotIP
        print(self.IP)
        PORT = 9559
        try:
            self.motion = ALProxy("ALMotion", self.IP, PORT)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e

        try:
            self.posture = ALProxy("ALRobotPosture", self.IP, PORT)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
       
        try:
            self.memory = ALProxy("ALMemory", self.IP, PORT)
        except Exception,e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e

        try:
            self.sonar = ALProxy("ALSonar", self.IP, PORT)
        except Exception, e:
            print "Could not create proxy to ALSonar"
            print "Error was: ", e

    #Paths
    LSONAR = "Device/SubDeviceList/US/Left/Sensor/Value"
    RSONAR = "Device/SubDeviceList/US/Right/Sensor/Value"
    ANGLEZ = "Device/SubDeviceList/InertialSensor/AngleZ/Sensor/Value" 

####---------------------

ReactToTouch = None
memory = None
flag = False
initialSentence = """ 
    Hola! 
"""

# NaoMotionBasket ------

def OpenHandBasket(gVars):
  names = list()
  times = list()
  keys = list()

  names.append("LElbowRoll")
  times.append([0.24])
  keys.append([-1.1612])

  names.append("LElbowYaw")
  times.append([0.24])
  keys.append([-1.66903])

  names.append("LHand")
  times.append([0.24])
  keys.append([0.7524])

  names.append("LShoulderPitch")
  times.append([0.24])
  keys.append([1.21335])

  names.append("LShoulderRoll")
  times.append([0.24])
  keys.append([-0.069072])

  names.append("LWristYaw")
  times.append([0.24])
  keys.append([-1.24718])

  names.append("RElbowRoll")
  times.append([0.24])
  keys.append([1.00788])

  names.append("RElbowYaw")
  times.append([0.24])
  keys.append([0.849794])

  names.append("RHand")
  times.append([0.24])
  keys.append([0.0724])

  names.append("RShoulderPitch")
  times.append([0.24])
  keys.append([1.69971])

  names.append("RShoulderRoll")
  times.append([0.24])
  keys.append([-0.251618])

  names.append("RWristYaw")
  times.append([0.24])
  keys.append([-0.105888])

  try:
    # uncomment the following line and modify the IP if you use this script outside Choregraphe.
    # motion = ALProxy("ALMotion", IP, 9559)
    gVars.motion.angleInterpolation(names, keys, times, True)
  except BaseException, err:
    print err

def CloseHandBasket(gVars):
  names = list()
  times = list()
  keys = list()

  names.append("LElbowRoll")
  times.append([0.72])
  keys.append([-1.13205])

  names.append("LElbowYaw")
  times.append([0.72])
  keys.append([-1.64602])

  names.append("LHand")
  times.append([0.72])
  keys.append([0.2576])

  names.append("LShoulderPitch")
  times.append([0.72])
  keys.append([1.26091])

  names.append("LShoulderRoll")
  times.append([0.72])
  keys.append([-0.0567999])

  names.append("LWristYaw")
  times.append([0.72])
  keys.append([-1.20116])

  names.append("RElbowRoll")
  times.append([0.72])
  keys.append([0.997142])

  names.append("RElbowYaw")
  times.append([0.72])
  keys.append([0.906552])

  names.append("RHand")
  times.append([0.72])
  keys.append([0.0928])

  names.append("RShoulderPitch")
  times.append([0.72])
  keys.append([1.58927])

  names.append("RShoulderRoll")
  times.append([0.72])
  keys.append([-0.283832])

  names.append("RWristYaw")
  times.append([0.72])
  keys.append([-0.0844119])

  try:
    gVars.motion.angleInterpolation(names, keys, times, True)

  except BaseException, err:
    print err


def finalHandMove(gVars):

  names = list()
  times = list()
  keys = list()

  names.append("LElbowRoll")
  times.append([0.2, 0.48])
  keys.append([-0.644238, -0.889678])

  names.append("LElbowYaw")
  times.append([0.2, 0.48])
  keys.append([-1.61074, -1.65369])

  names.append("LHand")
  times.append([0.2, 0.48])
  keys.append([0.2088, 0.2088])

  names.append("LShoulderPitch")
  times.append([0.2, 0.48])
  keys.append([0.765424, 0.937232])

  names.append("LShoulderRoll")
  times.append([0.2, 0.48])
  keys.append([0.0383081, 0.101202])

  names.append("LWristYaw")
  times.append([0.2, 0.48])
  keys.append([1.54623, -1.5862])

  names.append("RElbowRoll")
  times.append([0.2, 0.48])
  keys.append([0.595234, 0.595234])

  names.append("RElbowYaw")
  times.append([0.2, 0.48])
  keys.append([1.04001, 1.04001])

  names.append("RHand")
  times.append([0.2, 0.48])
  keys.append([0.0608, 0.0608])

  names.append("RShoulderPitch")
  times.append([0.2, 0.48])
  keys.append([1.48802, 1.48802])

  names.append("RShoulderRoll")
  times.append([0.2, 0.48])
  keys.append([-0.257754, -0.257754])

  names.append("RWristYaw")
  times.append([0.2, 0.48])
  keys.append([0.757754, 0.757754])

  try:
    # uncomment the following line and modify the IP if you use this script outside Choregraphe.
    # motion = ALProxy("ALMotion", IP, 9559)
    gVars.motion.angleInterpolation(names, keys, times, True)
 
  except BaseException, err:
    print err

# NaoMotionBasket ------


# ValidateNaoMark --------------

def readNaoMark():

  # Create a proxy to ALLandMarkDetection
  try:
    landMarkProxy = ALProxy("ALLandMarkDetection")
  except Exception, e:
    print "Error when creating landmark detection proxy:"
    print str(e)
    exit(1)

  # Subscribe to the ALLandMarkDetection proxy
  # This means that the module will write in ALMemory with
  # the given period below
  period = 500
  landMarkProxy.subscribe("Test_LandMark", period, 0.0 )

  # ALMemory variable where the ALLandMarkdetection modules
  # outputs its results
  memValue = "LandmarkDetected"

  # Create a proxy to ALMemory
  try:
    memoryProxy = ALProxy("ALMemory")
  except Exception, e:
    print "Error when creating memory proxy:"
    print str(e)
    exit(1)
    
    global naoMarkDetected 
    #naoMarkDetected= 64
    #print "Nao Mark detected:"
    #print naoMarkDetected


  # A simple loop that reads the memValue and checks whether landmarks are detected.
  for i in range(0, 10):
    time.sleep(0.5)
    val = memoryProxy.getData(memValue)

    # Check whether we got a valid output.
    if(val and isinstance(val, list) and len(val) >= 2):
      # Second Field = array of Mark_Info's.
      markInfoArray = val[1]

      try:
        # Browse the markInfoArray to get info on each detected mark.
        for markInfo in markInfoArray:

          # Second Field = Extra info (ie, mark ID).
          markExtraInfo = markInfo[1]

          naoMarkDetected= markExtraInfo[0]

          return naoMarkDetected

      except Exception, e:
        print "Error msg %s" % (str(e))
    else:
        print "No landmark detected"


  # Unsubscribe the module.
  landMarkProxy.unsubscribe("Test_LandMark")

  print "Test terminated successfully."

# ValidateNaoMark --------------


# Vision --------------------------
def contoursFilter():

  ##-----Read Mask--------------------##
  img = cv2.imread('dilation3.png',0)
  ##-----Threshold Filter-------------##
  ret,thresh = cv2.threshold(img,127,255,0)
  ##-----Find contours-------------##
  contours,hierarchy = cv2.findContours(thresh, 1, 2)

  return contours

def redFilter(hsv):
    lower_range = np.array([0, 50, 50], dtype=np.uint8) #red color
    upper_range = np.array([10, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_range, upper_range)

    #Remove noise of the selected mask
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    erosion2 = cv2.erode(erosion, kernel, iterations=1)
    erosion3 = cv2.erode(erosion2, kernel, iterations=1)
    dilation = cv2.dilate(erosion3,kernel, iterations =1)
    dilation2 = cv2.dilate(dilation,kernel, iterations =1) 
    dilation3 = cv2.dilate(dilation2,kernel, iterations =1)

    #cv2.imshow('dilation3',dilation3)
    cv2.imwrite('dilation3.png', dilation3)

    contRed= contoursFilter()
    lenContRed= len(contRed)

    return lenContRed


def brownFilter(hsv):
  lower_range = np.array([20, 50, 50], dtype=np.uint8) 
  upper_range = np.array([40, 255, 255], dtype=np.uint8)

  mask = cv2.inRange(hsv, lower_range, upper_range)

  #Remove noise of the selected mask
  kernel = np.ones((5,5),np.uint8)
  erosion = cv2.erode(mask, kernel, iterations=1)
  erosion2 = cv2.erode(erosion, kernel, iterations=1)
  erosion3 = cv2.erode(erosion2, kernel, iterations=1)
  dilation = cv2.dilate(erosion3,kernel, iterations =1)
  dilation2 = cv2.dilate(dilation,kernel, iterations =1) 
  dilation3 = cv2.dilate(dilation2,kernel, iterations =1)

  dilation3Brown = dilation3
  # cv2.imshow('dilation3Brown',dilation3Brown)
  cv2.imwrite('dilation3.png', dilation3)

  contBrown= contoursFilter()
  
  lenContBrown= len(contBrown)

  return lenContBrown


def whiteFilter(hsv):
  lower_range = np.array([0, 0, 140], dtype=np.uint8) #red color
  upper_range = np.array([0, 255, 255], dtype=np.uint8)

  mask = cv2.inRange(hsv, lower_range, upper_range)

  #Remove noise of the selected mask
  kernel = np.ones((5,5),np.uint8)
  erosion = cv2.erode(mask, kernel, iterations=1)
  erosion2 = cv2.erode(erosion, kernel, iterations=1)
  erosion3 = cv2.erode(erosion2, kernel, iterations=1)
  dilation = cv2.dilate(erosion3,kernel, iterations =1)
  dilation2 = cv2.dilate(dilation,kernel, iterations =1) 
  dilation3 = cv2.dilate(dilation2,kernel, iterations =1)

  dilation3White = dilation3
  # cv2.imshow('dilation3White',dilation3White)
  cv2.imwrite('dilation3.png', dilation3)
  
  contWhite= contoursFilter()

  lenContWhite= len(contWhite)

  return lenContWhite
# Vision --------------------------



####---------------------####
#       MAIN ROUTINE  #
####---------------------####
def mainRoutine():
    # Greetings
    tts = ALProxy('ALTextToSpeech')

    # ---------- Speech Recognition ----------------- #
    asr = ALProxy('ALSpeechRecognition')
    tempMem = ALProxy('ALMemory')
    asr.setLanguage('Spanish')
    tts.say(initialSentence)
    vocabulary = ['si', 'no', 'porfavor']

    # ---------- Vision Recognition ----------------- #
    photoCP = ALProxy('ALPhotoCapture')
    photoCP.setResolution(2)
    photoCP.setPictureFormat('jpg')
    #cv2.imshow('nao9',img)
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    photoCP.takePictures(5,'/home/nao/pythonProjects', 'whitef')
    img = cv2.imread('whitef_5.jpg')#take the last image (the good one)
  
    #img = cv2.resize(img,(640,480))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray = cv2.threshold(gray,127,255,0)
    gray2 = gray.copy()

    height, width = img.shape[:2]

    red = [0] * 256
    green = [0] * 256
    blue = [0] * 256

    median = width*height*0.5

    for j in range(0,width):
      for i in range(0, height):
        index = int(img[i,j,2])
        red[index] += 1
        index = int(img[i,j,1])
        green[index] += 1
        index = int(img[i,j,0])
        blue[index] += 1

    redCounter = 0
    greenCounter = 0
    blueCounter = 0
    for i in range(0,255):
      redCounter+= red[i]
      if(redCounter >=  median):
        redCounter = i
        break
        
    for i in range(0,255):
      greenCounter+= green[i]
      if(greenCounter >=  median):
        greenCounter = i
        break

    for i in range(0,255):
      blueCounter+= blue[i]
      if(blueCounter >=  median):
        blueCounter = i
        break
        

    print redCounter
    print greenCounter
    print blueCounter

    if(redCounter>=130 and redCounter<=160 and greenCounter>=148 and greenCounter<=165 and blueCounter>=142 and blueCounter<= 168):
      print("white detected")


####---------------------####
#       END MAIN ROUTINE  #
####---------------------####



class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        # self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to TouchChanged event:
        global memory
        memory = ALProxy('ALMemory')
        memory.subscribeToEvent('MiddleTactilTouched',
            'ReactToTouch',
            'onTouchedStart')

    def onTouchedStart(self, strVarName, value):
        """ This will be called each time a touch
        is detected.
        """
        # Unsubscribe to the event when starts the routine,
        # to avoid repetitions
        memory.unsubscribeToEvent('MiddleTactilTouched',
            'ReactToTouch')
        
        mainRoutine() # This will be the main routine

        # Subscribe again to the event (RearTactilTouched)
        memory.subscribeToEvent('RearTactilTouched',
            'ReactToTouch',
            'onTouchedEnd')

    def onTouchedEnd(self, strVarName, value):
        # global variable to let the application that the routine has ended
        global flag
        flag = True

def main(ip, port):
    """ Main entry point
    """
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists

    #nao_ip= ip

    myBroker = ALBroker('myBroker',
       '0.0.0.0',   # listen to anyone
       0,           # find a free port and use it
       ip,          # parent broker IP
       port)        # parent broker port


    global ReactToTouch
    global flag
    ReactToTouch = ReactToTouch('ReactToTouch')

    try:
        while True:
            if flag:
                print
                print 'The routine has finished in a clean way.'
                myBroker.shutdown()
                sys.exit(0)
            
    except KeyboardInterrupt:
        print
        print 'Interrupted by user, shutting down'
        myBroker.shutdown()
        sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help='Robot ip address')
    parser.add_argument('--port', type=int, default=9559,
                        help='Robot port number')
    args = parser.parse_args()

    global nao_ip
    nao_ip= args.ip

    main(args.ip, args.port)