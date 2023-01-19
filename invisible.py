import cv2 as cv
import numpy as np

vid= cv.VideoCapture(0)
FirstFrame = True
while True:
    succ, frame = vid.read()
    if succ:
        if FirstFrame:
            F_Frame=frame
            FirstFrame= False
        else:
            mask=cv.inRange(frame,(10,10,0),(40,40,255))
            frame[mask>0]=F_Frame[mask>0]
        cv.imshow("Frame",frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cv.destroyAllWindows()
