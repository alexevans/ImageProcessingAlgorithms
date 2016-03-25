#run with python2 med_avg_filters.py <relative path of the image>
#<salt and pepper frequency as a decimal percent> 
#<standard deviation as integer for normally distributed noise> 
#<neightborhood size (must be odd)>

from copy import deepcopy
import numpy as np
import cv2
import random
import math
import sys

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

#applies ageraging filter to the image
def avg_filter(image1, neighborhood):
  x,y=image1.shape
  img2=deepcopy(image1)
  median=0
  #using an offset so it doesn't try to get the neighborhood of an edge pixel
  offset=(neighborhood-1)/2 
  for a in range(offset, x-offset):
    for b in range(offset, y-offset):
      median=int(np.average(get_kernel(img2, neighborhood, a, b)))
      img2[a,b]=median
  return img2



if __name__=='__main__':
  image1 = str(sys.argv[1])
  frequency = float(sys.argv[2])
  std_dev = int(sys.argv[3])
  nbhd = int(sys.argv[4])

  im1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
  imgauss=noise_gauss(im1, std_dev)
  imavg=avg_filter(imgauss, nbhd)
  imsp=noise_sp(im1, frequency)
  imedian=median_filter(imsp, nbhd)

  #calculate psnr for both images
  #65025 is 255^2, 255 is the maximum fluctuation in the image since using 0-255 grayscale
  diff_img=im1-imedian
  mse_median=((diff_img.sum())**2)/(im1.size) 
  psnr_median=10*(math.log10((65025)/mse_median))

  diff_img=im1-imavg
  mse_avg=((diff_img.sum())**2)/(im1.size)
  psnr_avg=10*(math.log10((65025)/mse_avg))

  #write generated images and PSNR results to files
  cv2.imwrite("OriginalLatest.png", im1)
  cv2.imwrite("SaltPepperNoiseLatest.png", imsp)
  cv2.imwrite("NormalNoiseLatest.png", imgauss)
  cv2.imwrite("MedianFilterLatest.png", imedian)
  cv2.imwrite("AverageFilterLatest.png", imavg)
  fil = open('psnrLatest.txt', 'w')
  fil.write('Median Filter PSNR: ' + str(psnr_median) + ' db')
  fil.write('\nAverage Filter PSNR: ' + str(psnr_avg) + ' db')
