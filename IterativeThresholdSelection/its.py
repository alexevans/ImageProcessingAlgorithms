#run with python2 its.py <relative path of the image>
#outputs a segmented binary image calculated using Iterative Threshold Selection

from copy import deepcopy
import numpy as np
import cv2
import sys

#Returns the histogram of the image as an array
def findHisto(image1):
  x, y = image1.shape
  hist = np.zeros(256)
  for a in xrange(x): 
    for b in xrange(y):
      hist[image1[a, b]] = hist[image1[a, b]]+1 #each intensity has its own slot in the hist array
  return hist

#Calculates the mean gray value in a histogram array from indices begin to end
def meanGrayLevel(hist, begin, end):
  total=0
  total_pix=0
  for x in range(begin, end):
    #add the index(gray level) * number of pixels(hist[x]) to the total
    total = total + (x*hist[x])
    total_pix = total_pix + hist[x] 
  #divide by total number of gray levels 
  total = int(total/total_pix)
  return total

#Calculates the appropriate threshold using Iterative Threshold Selection
def calcThresh(hist):
  #first guess is mean gray level of entire image
  guess = meanGrayLevel(hist, 0, hist.size-1)
  #get the averages of gray levels above and below guess
  upper_avg = meanGrayLevel(hist, guess, hist.size-1)
  lower_avg = meanGrayLevel(hist, 0, guess-1)
  avg = int((upper_avg+lower_avg)/2)
  if(avg==guess):
    return guess
  while(avg!=guess):
   guess = avg
   upper_avg = meanGrayLevel(hist, guess, hist.size)
   lower_avg = meanGrayLevel(hist, 0, guess-1)
   avg = int((upper_avg+lower_avg)/2)
  return guess   
  
#Calls calcThresh and applies the calculated threshold and returns the binary image
def getThreshImage(im1):
  histo = findHisto(im1)
  thresh = calcThresh(histo)
  im2 = deepcopy(im1)
  x, y = im2.shape
  for a in xrange(x):
    for b in xrange(y):
      if(im2[a][b]<thresh):
        im2[a][b]=0
      else:
        im2[a][b]=255
  return im2


if __name__=='__main__':
  image1 = str(sys.argv[1])
  im1 = cv2.imread(image1)
  im3 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
  image_Thresh = getThreshImage(im3) 
  cv2.imwrite("Segmented_latest.png", image_Thresh)

