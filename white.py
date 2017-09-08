import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([0,0,140])
    upper_blue = np.array([0,255,255])
    
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    kernel = np.ones((10,10),np.uint8)
    #erosion = cv2.erode(mask, kernel, iterations=1)
    #erosion2 = cv2.erode(erosion, kernel, iterations=1)
    #erosion3 = cv2.erode(erosion2, kernel, iterations=1)
    dilation = cv2.dilate(mask,kernel, iterations =1)
    #dilation2 = cv2.dilate(dilation,kernel, iterations =1) 
    #dilation3 = cv2.dilate(dilation2,kernel, iterations =1)
     
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('dilation1',dilation)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
