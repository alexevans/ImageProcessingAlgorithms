#run with python2 lce.py <relative path of the image>

from copy import deepcopy
import numpy as np
import cv2
import sys

#Iterate through all pixels in image1 and count the number of times each intensity appears
def findHisto(image1):
  x, y = image1.shape
  hist = np.zeros(256)
  for a in xrange(x): 
    for b in xrange(y):
      hist[image1[a, b]] = hist[image1[a, b]]+1 #each intensity has its own slot in the hist array
  return hist

#performs linear contrast enhancement on an image 
def lce(image1, blow, bhigh):
  x, y = image1.shape
  image2 = deepcopy(image1)#copy by value, not reference to preserve original image
  for a in xrange(x):
    for b in xrange(y):
      if (image1[a, b]<=blow):#if the pixel is below the threshold set to black
        image2[a, b]=0
      elif (image1[a, b]>=bhigh):#if the pixel is above the threshold set to white
        image2[a, b]=255
      else:#if the pixel in inside the threshold, scale it
        image2[a, b] = (int((float(image1[a, b]-blow)/float(bhigh-blow))*255))
  return(image2)

#nothing method, used for calling cv2.createTrackBar
def none(a):
  pass

#performs automatic contrast enhancement on image1 with histogram histo to the percent percent
def ace(image1, histo, percent):
  low=0
  high=0
  total=0
  p = float(float(float(percent)/100)*image1.size)#scale percent to the image
  for x in xrange(0, 255): #find the blow by summing up values starting from the bottom until their percentage is >= percent
    total = total + histo[x]
    if (total>=p):
      low = x
      break
  total=0
  for y in xrange(0, 255): #find the bhigh by summing up values starting from the top until their percentage is >= percent
    total = total + histo[255-y]
    if (float(total)>=p):
      high = 255-y
      break
  return (low, high)


if __name__=='__main__':
  #create windows, trackbars, and initialize variables
  cv2.namedWindow('Linear Contrast Enhancement')
  im1 = cv2.imread(str(sys.argv[1]), cv2.IMREAD_GRAYSCALE)
  hist = findHisto(im1)
  im2 = deepcopy(im1)
  cv2.imshow("Linear Contrast Enhancement", im1)
  cv2.createTrackbar('Auto/Manual(0/1): ', 'Linear Contrast Enhancement', 0, 1, none)
  cv2.createTrackbar('Percent', 'Linear Contrast Enhancement', 0, 100, none)
  cv2.createTrackbar('Low', 'Linear Contrast Enhancement', 0, 255, none)
  cv2.createTrackbar('High', 'Linear Contrast Enhancement', 255, 255, none)
  lastlow=0
  lasthigh=0
  high = 0
  low = 0
  lastpercent = 0
  percent = 0
  am = 0
  l = 0
  h = 0

  #main program loop. If in auto mode, the percent slider makes adjusts contrast with ace, if in manual mode, low and high sliders make adjustments with lce 
  while (True):
    low = cv2.getTrackbarPos('Low', 'Linear Contrast Enhancement')
    high = cv2.getTrackbarPos('High', 'Linear Contrast Enhancement')
    percent = cv2.getTrackbarPos('Percent', 'Linear Contrast Enhancement')
    am = cv2.getTrackbarPos('Auto/Manual(0/1): ', 'Linear Contrast Enhancement')
    if (am == 0): #automatic mode
      if (percent!=lastpercent):
        l, h=ace(im1, hist, percent)
        cv2.setTrackbarPos('Low', 'Linear Contrast Enhancement', l)
        cv2.setTrackbarPos('High', 'Linear Contrast Enhancement', h)
        im2=lce(im1, low, high)
        lastpercent = percent
        lastlow = l
        lasthigh = h
    elif (am ==1): #manual mode
      if (lastlow!=low or lasthigh!=high):
        im2=lce(im1, low, high)
        lastlow=low
        lasthigh=high
    cv2.imshow("Linear Contrast Enhancement", im2) #display image after corrections
    cv2.waitKey(2000) #loop delay
  cv2.destroyAllWindows()
