# -*- coding: utf-8 -*-
"""Action and gesture Recognition.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kLhaNKA0q2_GImKN2ycYY0yp8X8YS-zf

**Detecting body points**

importing libaries
"""

import cv2
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow
import numpy as np

"""**Loading the image**"""

from google.colab import drive
drive.mount('/content/drive')

image=cv2.imread('/content/drive/MyDrive/Computer Vision Masterclass/Images/megan.jpg')

cv2_imshow(image)

image.shape ,image.shape[0] * image.shape[1]

image_blob=cv2.dnn.blobFromImage(image=image,scalefactor=1.0/255,
                                 size=(image.shape[1],image.shape[0])) # normalizing data to blob fromat

"""**Loading the pre_train neural Network**"""

network=cv2.dnn.readNetFromCaffe('/content/drive/MyDrive/Computer Vision Masterclass/Weights/pose_deploy_linevec_faster_4_stages.prototxt',
                                 '/content/drive/MyDrive/Computer Vision Masterclass/Weights/pose_iter_160000.caffemodel')

len(network.getLayerNames())

"""**Predicting body points**"""

network.setInput(image_blob)
output=network.forward()

output.shape

position_width=output.shape[3]
position_height=output.shape[2]

num_points=15
points=[]
threshold=0.1
for i in range(num_points):
  confidence_map = output[0, i,:,:]
  _, confidence, _, point =cv2.minMaxLoc(confidence_map)
  #print(confidence)
  #print(point)

  x=int((image.shape[1]*point[0])/position_width)
  y=int((image.shape[0]*point[1])/position_height)

  if confidence > threshold:
    cv2.circle(image,(x,y),5,(0,0,255), thickness=-1)
    cv2.putText(image,'{}'.format(i),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255))
    points.append((x,y))
  else:
    points.append(None)

plt.figure(figsize=(14,10))
plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB));

point_connection= [[0,1],[1,2],[2,3],[3,4],[1,5],[5,6],[6,7],[1,14],[14,8],[8,9],[9,10],[14,11],[11,12],[12,13]]

point_connection

for connect in point_connection:
  partA = connect[0]
  partB = connect[1]

  if points[partA] and points[partB]:
    cv2.line(image,points[partA],points[partB],(0,255,0),1)

plt.figure(figsize=(14,10))
plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB));

"""**Detecting Movement**"""

image2 = cv2.imread('/content/drive/MyDrive/Computer Vision Masterclass/Images/player.jpg')
cv2_imshow(image2)

image2 = cv2.imread('/content/drive/MyDrive/Computer Vision Masterclass/Images/player.jpg')
image_blob2=cv2.dnn.blobFromImage(image=image2,scalefactor=1.0/255,size=(image2.shape[1],image2.shape[0]))
network.setInput(image_blob2) #Neural Network
output=network.forward()
position_width=output.shape[3]
position_height=output.shape[2]

num_points=15
points=[]
threshold=0.1
for i in range(num_points):
  confidence_map = output[0, i,:,:]
  _, confidence, _, point =cv2.minMaxLoc(confidence_map)
  x=int((image2.shape[1]*point[0])/position_width)
  y=int((image2.shape[0]*point[1])/position_height)

  if confidence > threshold:
    cv2.circle(image2,(x,y),4,(255,0,255), thickness=-1)
    cv2.putText(image2,'{}'.format(i),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
    cv2.putText(image2,'{} - {}'.format(point[0],point[1]),(x,y+10),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
    points.append((x,y))
  else:
    points.append(None)

plt.figure(figsize=(14,10))
plt.imshow(cv2.cvtColor(image2,cv2.COLOR_BGR2RGB));

def verify_movement(points):
  head,right_wrist,left_wrist= 0,0,0
  for i, point in enumerate(points):
    if i == 0:
      head = point[1]
    elif i == 4:
      right_wrist = point[1]
    elif i == 7:
      left_wrist = point[1]

  if right_wrist < head and left_wrist < head:
    print('Player arm are above head')
  else:
    print('Player arm are not above head')

verify_movement(points)

"""# **Detecting if legs are Apart**"""

image2 = cv2.imread('/content/drive/MyDrive/Computer Vision Masterclass/Images/jump.jpg')
cv2_imshow(image2)

image3= cv2.imread('/content/drive/MyDrive/Computer Vision Masterclass/Images/jump.jpg')
cv2_imshow(image3)
image_blob3=cv2.dnn.blobFromImage(image=image3,scalefactor=1.0/255,size=(image2.shape[1],image2.shape[0]))
network.setInput(image_blob3) #Neural Network
output=network.forward()
position_width=output.shape[3]
position_height=output.shape[2]

num_points=15
points=[]
threshold=0.1
for i in range(num_points):
  confidence_map = output[0, i,:,:]
  _, confidence, _, point =cv2.minMaxLoc(confidence_map)
  x=int((image3.shape[1]*point[0])/position_width)
  y=int((image3.shape[0]*point[1])/position_height)

  if confidence > threshold:
    cv2.circle(image3,(x,y),4,(255,0,255), thickness=-1)
    cv2.putText(image3,'{}'.format(i),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
    cv2.putText(image3,'{} - {}'.format(point[0],point[1]),(x,y+10),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
    points.append((x,y))
  else:
    points.append(None)

plt.figure(figsize=(14,10))
plt.imshow(cv2.cvtColor(image3,cv2.COLOR_BGR2RGB));

def verify_legs_apart(points):
  left_hip,right_hip= 0,0
  right_leg,left_leg= 0,0,

  for i, point in enumerate(points):
    if i == 11:
      right_hip = point[0]
    elif i == 8:
      left_hip = point[0]
    elif i == 13:
      right_leg = point[0]
    elif i == 10:
      left_leg = point[0]

  if (right_leg > right_hip) and (left_leg < left_hip):
    print('Leg apart')
  else:
    print('Legs not apart')

verify_legs_apart(points)

