#run with python2 robers_sobel_edge.py <relative path of the image>
#outputs the original image, the image after Roberts, and the image after Sobel

from copy import deepcopy
import numpy as np
import cv2
import sys

#This calculates using Roberts' Operator for image1 and returns the image calculated 
def getRoberts(image1):
  image2 = deepcopy(image1)
  #get dimensions and iterate through the image, leaving out the edge rows and columns
  x, y = image2.shape
  for a in range(1, x-1):
    for b in range(1, y-1):
      #calculate the new value for each pixel
      grad = abs(int(image2[a,b])-int(image2[a+1,b+1]))+abs(int(image2[a, b+1])-int(image2[a+1,b]))
      image2[a,b] = grad
  return image2

#This calculates using the Sobel Algorithm for image1 and returns the image calculated 
def getSobel(image1):
  image2 = deepcopy(image1)
  #get dimensions and iterate through the image, leaving out 2 edge rows and columns, since sobel uses 3x3
  x, y = image2.shape
  for a in range(2, x-2):
    for b in range(2, y-2):
      #calculate the new value for each pixel
      grad_horiz = ((-1*image1[a-1, b-1])+(-2*image1[a-1, b])+(-1*image1[a-1, b+1])) + (image1[a+1, b-1]+(2*image1[a+1, b])+image1[a+1, b+1])
      grad_vert = ((-1*image1[a-1, b-1])+(-2*image1[a, b-1])+(-1*image1[a+1, b-1])) + (image1[a-1, b+1]+(2*image1[a, b+1])+image1[a-1, b+1])
      image2[a,b] = abs(grad_horiz)+abs(grad_vert)
  return image2


if __name__=='__main__':
  image1 = str(sys.argv[1])
  im1 = cv2.imread(image1)
  im3 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
  image_Roberts = getRoberts(im3) 
  image_Sobel = getSobel(im3)
  cv2.imwrite("Roberts_latest.png", image_Roberts)
  cv2.imwrite("Sobel_latest.png", image_Sobel)

