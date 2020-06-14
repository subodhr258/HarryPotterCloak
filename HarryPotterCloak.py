#import libraries:
import cv2
import numpy as np 
import time

#output video:
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc,20.0, (640,480))

#read from webcam:
cap = cv2.VideoCapture(0)

#allow the system to sleep for 3 seconds before the webcam starts:
time.sleep(3)
count=0
background=0

#capture the background in range of 60:
for i in range(60):
	ret,background = cap.read()
background = np.flip(background, axis=1) #so we have mirroring

#read every frame from webcam till the camera is open:
while(cap.isOpened()):
	ret,img = cap.read()
	if not ret:
		break
	count+=1
	img = np.flip(img,axis=1)

	#convert the color space from bgr to hsv:
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	#HSV means Hue, Saturation, Value/Brightness.
	#IMP: Hue of 0 - 360 is divided into 2 of 0 - 180, and saturation & Value are normalized to 0 - 255.
	#generate masks to detect red color:
	lower_red = np.array([0,120,50])
	upper_red = np.array([10,255,255])
	mask1 = cv2.inRange(hsv,lower_red,upper_red)

	lower_red = np.array([170,120,50])
	upper_red = np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)

	mask1 = mask1+mask2

	#open and dilate the mask image:
	mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
	mask1 = cv2.morphologyEx(mask1,cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

	#create an inverted mask to segment out the red color of the frame:
	mask2 = cv2.bitwise_not(mask1)

	#segment the red color part out of the frame using bitwise and within the inverted mask

	res1 = cv2.bitwise_and(img,img,mask=mask2)

	#create image showing static background framw pixels only for the masked region

	res2 = cv2.bitwise_and(background,background, mask=mask1)

	#generating the final output and writing video output:
	finalOutput = cv2.addWeighted(res1,1,res2,1,0)
	#out.write(finalOutput)
	cv2.imshow("Magic",finalOutput)
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
out.release()
cv2.destroyAllWindows()