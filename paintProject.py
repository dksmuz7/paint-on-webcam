# Color detection and drawing on the screen
# Importing the required module

import cv2 as cv
import numpy as np

# creating points list
myPoints = [] # [x,y,colorId]


# Creating color database (lists)
colorsAvl = [[90,109,49,147,255,255],[10,179,0,255,0,255],[15,179,0,255,0,255]]
colorValue = [[255,0,0],[0,255,0],[0,0,255]]

# Creating draw on canvas function
def drawOnCanvas(myPoints,colorValues):
    for point in myPoints:
        cv.circle(resultedImg,(point[0],point[1]),5,colorValues[point[2]],cv.FILLED)

# Get contour function
def getContours(img):
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area>50:
            print()
            print("Area =",area)
            # cv.drawContours(resultedImg,cnt,-1,(0,255,0),2)
            peri = cv.arcLength(cnt,True)
            approx = cv.approxPolyDP(cnt,0.02*peri,True)
            # creating bounding box around the detected images
            x,y,w,h = cv.boundingRect(approx)
            # cv.rectangle(resultedImg,(x,y),(x+w,y+h),(0,255,0),2)
    return x+w//2,y

# Finding color and start drawing over the image
def findColor(img,colorsAvl,colorValues):
    hsvImg = cv.cvtColor(img,cv.COLOR_BGR2HSV)

    count = 0
    newPoints = []
    for color in colorsAvl:
        lowerLimit = np.array(color[0:3])
        upperLimit = np.array(color[3:6])
        mask = cv.inRange(hsvImg,lowerLimit,upperLimit)
        x,y=getContours(mask)
        cv.circle(resultedImg,(x,y),5,colorValues[count],cv.FILLED)

        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count += 1
    return newPoints


# Access the webcam
frameWidth = 620
frameHeight = 480
brightness = 100

webcam = cv.VideoCapture(0)
webcam.set(3,frameWidth)   # width
webcam.set(4,frameHeight)  # height
webcam.set(10,brightness)  # britness

while True:
    success, img = webcam.read()
    resultedImg = img.copy()

    newPoints = findColor(img,colorsAvl,colorValue)
    if len(newPoints) != 0:
        for newPoint in newPoints:
            myPoints.append(newPoint)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints,colorValue)

    cv.imshow("Resulted video",resultedImg)

    # To quit
    if cv.waitKey(1) & 0xFF == ord("q"):
        break


