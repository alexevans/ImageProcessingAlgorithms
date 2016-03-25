# ImageProcessingAlgs
Implementations of various image processing algorithms.

##LinearContrastEnhancement
Adjusts an image's contrast. There are two modes: Auto and Manual. 
Manual uses linear contrast enhancement, which scales the contrast between the input low and high values to the full range of contrast of the image (in this case, we have grayscale images with a value of 0-255 for each pixel), sets everything below the low value to the minimum and everything above the high value to the maximum. Auto gets a range for the low and high thresholds for linear contrast enhancement using the input percentage. Auto will find the low and high values at which the entered percent of pixels in the image are below low and above high and run linear contrast enhancement on the image using these low and high thresholds.

Run with python2 lce.py \<relative path to image file\>

##MedianAndAveragingFilters
Median Filter and Averaging Filter for noise reduction. First noise is added to the input image, randomly distributed 'salt and pepper' noise for filtering with the median filter with a specified frequency, and gaussian intensity noise for filtering with the averaging filter. The Median filter sets the pixels in a kernel to the median value of the kernel. The Averaging filter sets the pixels in a kernel to the average value of the kernel. 

Run with python2 med_avg_filters.py \<relative path to image file\> \<frequency for salt and pepper noise(percent expressed as a decimal)\> \<standard deviation for gaussian noise(integer)\> \<size of the kernel(odd integer)\> 

Outputs: A grayscale image of the original image, the image with salt and pepper noise, the image with gaussian noise, the salt and pepper image after median filtering, the gaussian image after average filtering, and a file containing the calculated values of PSNR (Peak Signal to Noise Ratio) for each filtered image as compared to the original grayscale image.

##RobertsAndSobelEdge
Roberts and Sobel edge detection. Roberts applies the 2x2 Roberts cross operator to the image, while Sobel applies the 3x3 Sobel operator. More information can be found at: <a href="https://en.wikipedia.org/wiki/Roberts_cross" target="_blank">Roberts Cross</a> <a href="https://en.wikipedia.org/wiki/Sobel_operator" target="_blank">Sobel operator</a>

Run with python2 roberts_sobel_edge.py \<relative path to image\>

Outputs: The image after Roberts edge detection and the image after Sobel edge detection.

##IterativeThresholdSelection
Iterative threshold attempts to find a good threshold to separate the image into two classes iteratively. It initially guesses that the best threshold is the mean pixel value in the image. It then compares this guess to the average of the average of the pixels above the threshold and the average of the pixels below the threshold, taking this new average as its next guess. It repeats this process until the the new average converges with its previous guess.

Run with python2 its.py \<relative path to image\>

Outputs: The segmented binary image after Iterative Threshold Selection

##VectorMedianFilter
On a multi-channel image such as a RGB color image, applying the Median Filter to each separate color channel can introduce colors to the output image that were not present in the original image. To fix this, we can combine the color channels into vectors so that each pixel is a vector. Then we can compare the euclidean distance between vectors in a kernel to get the median vector. Since the median vector will always be a RGB combination that was in the original image, we won't add any fake colors to the image.

Run with python2 vmf.py \<relateice path to image\> \<frequency of noise(percent expressed as a decimal)\> \<size of the kernel(odd integer)\>

Outputs: The image with noise added, the image filtered with median filter on individual color channels, the image filtered with vector median filter, a file containing the PSNR of the two filtered images   
