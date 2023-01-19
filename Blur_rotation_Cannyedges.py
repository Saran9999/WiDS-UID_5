import numpy
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    if ret:
        # mask=cv2.inRange(frame,(0,0,0),(50,25,255))
        # frame[mask>0]=[255,0,0]
        # cv2.imshow('frame',frame)
        # Finding edges
        edges=cv2.Canny(frame,100,250)
        cv2.imshow("Edges", edges)
        blur=cv2.GaussianBlur(frame,(5,5),0)
        rotation=cv2.flip(frame,1)
        # video mirror to original
        cv2.imshow("mirror",rotation)
        # Gaussian Blur
        cv2.imshow("Blur", blur)
        # print(edges)
        # img=frame+edges
        # cv2.imshow("com",img)
        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (255, 0, 255), 1)
        # adding colours to edges
        cv2.imshow('Contours', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cv2.destroyAllWindows()