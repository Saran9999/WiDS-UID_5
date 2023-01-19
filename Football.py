import cv2 as cv
import numpy as np

vid=cv.VideoCapture('FootBall.mp4')
#green range
lower_green = np.array([40,40, 40])
upper_green = np.array([70, 255, 255])
#white range
lower_white = np.array([0,0,200])
upper_white = np.array([255,15,255])
while True:
    Succ , frame =vid.read()
    if not Succ:
        #print("Frame not found")
        break
    df=cv.GaussianBlur(frame,(5 ,5),0)
    #df=frame
    hsv= cv.cvtColor(df , cv.COLOR_BGR2HSV)
    mask= cv.inRange(hsv,lower_green,upper_green)
    res = cv.bitwise_and(df, df, mask=mask)
    #cv.imshow("blur",df)
	#convert to hsv to gray
    res_bgr = cv.cvtColor(res,cv.COLOR_HSV2BGR)
    res_gray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    kernel = np.ones((5,5),np.uint8)
    thresh = cv.threshold(res_gray,127,255,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    # cv.imshow("Debugging",thresh)
    thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
    thresh = cv.dilate(thresh,kernel,iterations = 3)
    thresh = cv.erode(thresh,kernel,iterations = 1)
    #cv.imshow("Debugging",thresh)
    contours,hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    prev = 0
    font = cv.FONT_HERSHEY_SIMPLEX
    num=0
    for c in contours:
        x,y,w,h = cv.boundingRect(c)
        if((h>=70 and w>=70) and (h<=120 and w<=120)) and ((h/w > 0.95 or w/h > 0.95) and (w/h < 1.1 or h/w < 1.1)) :
            #cv.imshow("Debugging",frame)
            player_img = frame[y:y+h,x:x+w]
            player_hsv = cv.cvtColor(player_img,cv.COLOR_BGR2HSV)
            #white ball  detection
            mask1 = cv.inRange(player_hsv, lower_white, upper_white)
            res1 = cv.bitwise_and(player_img, player_img, mask=mask1)
            res1 = cv.cvtColor(res1,cv.COLOR_HSV2BGR)
            res1 = cv.cvtColor(res1,cv.COLOR_BGR2GRAY)
            nzCount = cv.countNonZero(res1)
            approx=cv.approxPolyDP(c, 0.04 * cv.arcLength(c, True), True)
            k=cv.isContourConvex(approx)
            # print(k)
            #print(nzCount)
            #cv.imshow("Debugging",res1)
            # cv.putText(frame, 'football', (x-2, y-2), font, 0.8, (0,255,0), 2, cv.LINE_AA)
            # cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            if (nzCount >= 40 and k and len(approx)> 4):
                # detect football
                #print("fuck off")
                num = num+1
                cv.putText(frame, 'football', (x-2, y-2), font, 0.8, (0,255,0), 2, cv.LINE_AA)
                cv.rectangle(frame,(x-1,y-1),(x+w+1,y+h+1),(0,255,0),3)
        # approx=cv.approxPolyDP(c, .03 * cv.arcLength(c, True), True)
        # if len(approx)==8:
        #     k=cv.isContourConvex(approx)
        #     if k:
        #         cv.putText(frame, 'football', (x-2, y-2), font, 0.8, (0,255,0), 2, cv.LINE_AA)
        #         cv.rectangle(frame,(x-1,y-1),(x+w+1,y+h+1),(0,255,0),3)
    # for Debugging for multiple times to show football
    # if num> 1:
    #     print(num)

    cv.imshow('Foot Ball Detection',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()