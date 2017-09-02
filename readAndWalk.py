
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
    photoCP.takePictures(5,'/home/nao/pythonProjects', 'nao')
    img=cv2.imread('nao_4.jpg')  #take the last image (the good one)
    #cv2.imshow('nao9',img)
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    tts.say("Ahora empecemos")
    sleep(1)
    repeatRed=1

    photoCP.takePictures(5,'/home/nao/pythonProjects', 'nao')
    img=cv2.imread('nao_4.jpg') 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sleep(1)
    
    l0=redFilter(hsv)
    l1=brownFilter(hsv)
    l2=whiteFilter(hsv)  
      
    if l0 != 0 or l1 != 0 or l2 != 0:
      l=[l0,l1,l2] #pone en la ultima posicion el color mas grande leido
      l.sort()
      print("l array:")
      print(l);

      colorDetected= l[2] #poner el nombre del color de la longitud mas larga

      if colorDetected == l0: #color rojo
        tts.say("Es una lata")
        naoMarkValue= 64
        print("Red detected")
        
      elif (colorDetected == l1): #color cafe
        tts.say("Es carton")
        naoMarkValue = 108
        print("Brown detected")

      elif (colorDetected == l2):#color blanco
        tts.say("Es plastico")
        naoMarkValue = 80
        print("White detected")   

      else:
        print("No color detected")

     # ---------- Vision Recognition ----------------- #

    
    #Define NaoMarks
    naoMarkValue=64
    naoMarkDetected=0

    #Initialize global variables
    gVars = globalVariables(nao_ip)

    #Nao Initial posture
    gVars.posture.goToPosture("StandInit",0.5) 
    initialAngle= gVars.memory.getData(gVars.ANGLEZ) #initialAngle
    
    #Begins walk
    #agregar lo del brazo
    #gVars.motion.
    gVars.motion.moveTo(0, 0, (math.pi)-0.4) #gira 180
    gVars.motion.moveTo(0.4, 0, 0)
    
## Select Path -------------------------

    #Read NaoMarks
    value= readNaoMark() #aqui es cuando ve primero la 80 (cafe)
    print value

    if value == naoMarkValue:
      print"este es el camino"
      gVars.motion.moveTo(0.45, 0, 0)

    else:
      gVars.motion.moveTo(0, 0, -(math.pi/6))#gira para valida la 108 (blanco)
      value= readNaoMark()
      print value

      if value == naoMarkValue:
        print"este es el camino"
        gVars.motion.moveTo(0.95, 0, 0)

      else: # esta es cuando debe de ir a al naoMark 64
        gVars.motion.moveTo(0, 0, (math.pi/6))
        gVars.motion.moveTo(0, 0, (math.pi/6))
        print" voy en camino" 
        gVars.motion.moveTo(0.95, 0, 0)
       
## Select Path -------------------------
      ''' 

    while (True):
        
        actRelTheta = gVars.memory.getData(gVars.ANGLEZ)
        
        print" actual valor theta"
        print actRelTheta

        print" initial "
        print initialAngle

        sleep(1)
'''


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
