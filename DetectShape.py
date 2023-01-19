import cv2
import numpy as np

# reading image
img = cv2.imread('shapes.png')
img = cv2.resize(img, (0,0), fx=2.5, fy=2.5) 
#blur=cv2.GaussianBlur(img,(5 ,5),0)
# converting image into grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(1,1),0)
# setting threshold of gray image
_, threshold = cv2.threshold(gray, 194, 255, cv2.THRESH_BINARY)
threshold=cv2.GaussianBlur(threshold,(9 ,9),0)
cv2.imshow("fuck",threshold)
detected_circles = cv2.HoughCircles(gray, 
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
               param2 = 30, minRadius = 60, maxRadius = 100)
# using a findContours() function
contours, _ = cv2.findContours(
	threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# To detect the circles
if detected_circles is not None:
  
    # Convert the circle parameters a, b and r to integers.
	detected_circles = np.uint16(np.around(detected_circles))
	for pt in detected_circles[0, :]:
		a, b, r = pt[0], pt[1], pt[2]
		cv2.putText(img, 'Circle', (a, b),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
i = 0
# list for storing names of shapes
for contour in contours:

	# here we are ignoring first counter because
	# findcontour function detects whole image as shape
	if i == 0:
		i = 1
		continue

	# cv2.approxPloyDP() function to approximate the shape
	approx = cv2.approxPolyDP(
		contour, 0.01 * cv2.arcLength(contour, True), True)
	
	# using drawContours() function
	# cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

	# finding center point of shape
	M = cv2.moments(contour)
	if M['m00'] != 0.0:
		x = int(M['m10']/M['m00'])
		y = int(M['m01']/M['m00'])

	# putting shape name at center of each shape
	if len(approx) == 3:
		cv2.putText(img, 'Triangle', (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

	elif len(approx) == 4:
		cv2.putText(img, 'Quadrilateral', (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

	elif len(approx) == 5:
		cv2.putText(img, 'Pentagon', (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

	elif len(approx) == 6:
		cv2.putText(img, 'Hexagon', (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)


# displaying the image after drawing contours
cv2.imshow('shapes', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
