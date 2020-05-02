# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

HUE_VALUE = 170

#Lower/upper boundaries of target color
colorLower = (HUE_VALUE - 10, 100, 100)
colorUpper = (HUE_VALUE + 10, 255, 255)
 
#Get the camera
camera = cv2.VideoCapture(0)

while True:

    #Grab current frame
    (grabbed, frame) = camera.read()
 
    #Resize the frame, inverted ("vertical flip" w/ 180degrees),
    #Blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600)
    frame = imutils.rotate(frame, angle=180)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    #Construct a mask for the target color, then perform
    #a series of dilations and erosions to remove any small
    #blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    #Find contours in the mask and initialize the current
    #(x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
 
    #Only proceed if at least one contour was found
    if len(cnts) > 0:
        #Find the largest contour in the mask, then use
        #it to compute the minimum enclosing circle and
        #centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
 
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
