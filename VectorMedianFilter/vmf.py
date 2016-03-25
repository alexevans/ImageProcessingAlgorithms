#run with python2 vmf.py <realtive path of image> <frequency of noise> <kernel size(must be odd)>

from copy import deepcopy
import numpy as np
import cv2
import random
import math
import sys
from numpy.lib.function_base import vectorize
from numpy import Infinity

#gets the kernel of the given size (must be odd) around start_row and start_col
def get_kernel(arr1, size, start_row, start_col):
  offset=(size-1)/2
  begin_row = start_row-offset
  begin_col = start_col-offset
  #slices arr1 for size around index given by start_row and start_col
  arr=arr1[begin_row:begin_row+size, begin_col:begin_col+size]
  return(arr)

#adds salt and pepper noise to the image randomly with about frequency of freq, given as a percent
def noise_sp(image1, freq):
  im2=deepcopy(image1)#copy by value to avoid modification to original image
  is_high=True
  x,y = image1.shape
  for a in range(0,x):
    for b in range(0,y):
      if (random.random()<freq):
        if(is_high):
          im2[a,b]=255
          is_high=False
        else:
          im2[a,b]=0
          is_high=True
  return(im2)
  
def noise_sp_color(image1, freq):
  im2=deepcopy(image1)#copy by value to avoid modification to original image
  is_high=True
  x,y,z = image1.shape
  for a in range(0,x):
    for b in range(0,y):
      if (random.random()<freq):
        if(is_high):
          im2[a,b,:]=255
          is_high=False
        else:
          im2[a,b,:]=0
          is_high=True
  return(im2)
  
#adds normally distributed noise for whole image with standard deviation input in range of 0-255
def noise_gauss(image1, std_dev):
  #computes a normally distrubuted array of integers the size of image1
  img2=np.random.normal(0, std_dev, image1.shape).astype(int)
  img2 = cv2.convertScaleAbs(img2)
  img3=image1+img2
  return img3

#applies median filter to the image
def median_filter(image1, neighborhood):
  x,y=image1.shape
  img2=deepcopy(image1)
  median=0
  #using an offset so it doesn't try to get the neighborhood of an edge pixel
  offset=(neighborhood-1)/2 
  for a in range(offset, x-offset):
    for b in range(offset, y-offset):
      median=int(np.median(get_kernel(img2, neighborhood, a, b)))
      img2[a,b]=median
  return img2

def noise_color(image1, freq):
  im2=deepcopy(image1)#copy by value to avoid modification to original image
  is_high=True
  x,y,z = image1.shape
  for a in range(0,x):
    for b in range(0,y):
      if (random.random()<freq):
	for x in range(0,3):
          im2[a,b,x]=random.randint(0,255)
  return(im2)



def get_minimum_dist(image1, neighborhood, a, b):
    kern = get_kernel(image1, neighborhood, a, b)
    min_dist=np.Infinity#maximum distance should be around 3975 for 3 dimensional pixels from 0 to 255 for a 9 pixel neighborhood
    sum_dist=0
    for x in range(0,neighborhood):
        for y in range(0,neighborhood):
            sum_dist=0
            for c in range(0,neighborhood):
                for d in range(0,neighborhood):
                    distance = np.linalg.norm((kern[x][y][:]).astype(np.uint16)-kern[c][d][:].astype(np.uint16))
                    sum_dist=sum_dist+distance
            if(sum_dist<min_dist):
                min_dist=sum_dist
                min_pix=kern[x][y][:]
    return(min_pix)
            

#applies median filter to the image
def vector_median_filter(image1, neighborhood):
  x,y,z=image1.shape
  img2=deepcopy(image1)
  #using an offset so it doesn't try to get the neighborhood of an edge pixel
  offset=(neighborhood-1)/2 
  for a in range(offset, x-offset):
    for b in range(offset, y-offset):
      min_pix=get_minimum_dist(image1, neighborhood, a, b)
      img2[a][b][:]=min_pix
  return img2



if __name__ == '__main__':
    image1 = str(sys.argv[1])
    frequency = float(sys.argv[2])
    nbhd = int(sys.argv[3])
   
    im1 = cv2.imread(image1)
    
    #im_salt = noise_sp_color(im1, frequency)
    im_salt = noise_color(im1, frequency)

    b_salt,g_salt,r_salt = cv2.split(im_salt)
    
    b_med = median_filter(b_salt, nbhd)
    g_med = median_filter(g_salt, nbhd)
    r_med = median_filter(r_salt, nbhd)
    im_median = cv2.merge((b_med, g_med, r_med))
    
    im_vmed = vector_median_filter(im_salt, nbhd)
    
    cv2.imwrite("Noise.png", im_salt)
    cv2.imwrite("MedianFilter.png", im_median)
    cv2.imwrite("VectorMedianFilter.png", im_vmed)
    
    #195075 = (255^2)*3 the range of possible vector values
    diff_img=(im_salt-im_median)**2
    mse_median=diff_img.sum()/(im1.size) 
    psnr_median=10*(math.log10((195075)/mse_median))
    
    diff_img=(im_salt-im_vmed)**2
    mse_vmed=diff_img.sum()/(im1.size) 
    psnr_vmed=10*(math.log10((195075)/mse_vmed))
    
    fil = open('PSNR.txt', 'w')
    fil.write("Median Filter PSNR: " + str(psnr_median) + " db")
    fil.write("\nVector Median Filter PSNR: " + str(psnr_vmed) + " db")
    
    
