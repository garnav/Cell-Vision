# test_labels.py
# Arnav Ghosh
# 1st June 2017

import numpy
import math
import csv
import matplotlib.patches as mpatches
from matplotlib import pylab
from PIL import Image
from skimage.draw import circle_perimeter
from skimage.filters.thresholding import threshold_otsu, threshold_isodata, threshold_li
from skimage.measure import label, regionprops
from skimage.color import label2rgb
from skimage.morphology import dilation
from scipy import ndimage

im = Image.open("N_sperm/DSC_0464.jpg").convert('L')
im = numpy.array(im)

#remove noise
imGaus3 = ndimage.filters.gaussian_filter(im, 3)

#edge detection
imx = numpy.zeros(imGaus3.shape)
ndimage.filters.sobel(imGaus3,1,imx)
imy = numpy.zeros(imGaus3.shape)
ndimage.filters.sobel(imGaus3,0,imy)
edgeDetected = numpy.sqrt(imx**2+imy**2)

#thresholding and closing
binaryImage = 1.0 * (edgeDetected > threshold_isodata(edgeDetected))
dilated = dilation(binaryImage)
filledImage = ndimage.binary_fill_holes(dilated)

#labelling
labelImage = label(filledImage)
image_label_overlay = label2rgb(labelImage, image=filledImage)

fig, ax = pylab.subplots(figsize=(10, 6))
ax.imshow(image_label_overlay)

with open('DSC_0169.csv', 'w') as csvfile:
    fieldnames = ['object', 'area']
    counter = 0
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for region in regionprops(labelImage):
        #if region.filled_area >= math.pi*(40**2) and region.filled_area <= math.pi*(75**2):
        if region.equivalent_diameter >= 80 and region.equivalent_diameter <= 150 and region.extent >= 0.5: 
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                      fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
            #writer.writerow({'object': counter, 'area': region.filled_area})
            #counter = counter + 1
            print region.extent
        
pylab.show()