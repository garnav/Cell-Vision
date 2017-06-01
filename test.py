# test.py
# Arnav Ghosh
# 1st June 2017

import numpy
from PIL import Image
from matplotlib import pylab
from skimage.exposure import histogram
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter
from skimage.filters.thresholding import threshold_otsu, threshold_isodata, threshold_li
from scipy.ndimage import filters

im = Image.open("N_sperm/DSC_0102.jpg").convert('L')
im = numpy.array(im)

#remove noise
imGaus3 = filters.gaussian_filter(im, 3)

#edge detection
imx = numpy.zeros(im.shape)
filters.sobel(imGaus3,1,imx)
imy = numpy.zeros(im.shape)
filters.sobel(imGaus3,0,imy)
edgeDetected = numpy.sqrt(imx**2+imy**2)

#thresholding
binaryImage = 1.0 * (edgeDetected > threshold_isodata(edgeDetected))

# Detect two radii
hough_radii = numpy.arange(80, 150)
hough_res = hough_circle(image, hough_radii)

accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=5)

# Draw them
image = binaryImage.copy()
for center_y, center_x, radius in zip(cy, cx, radii):
    circy, circx = circle_perimeter(center_y, center_x, radius)
    image[circy, circx] = 6.0

pylab.imshow(image)
pylab.show()