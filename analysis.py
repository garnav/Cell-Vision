# analysis.py
# Arnav Ghosh
# 7th June 2017

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

class Analysis(object):
    
    THRESHOLD = 15.0
    MIN_DIAMETER = 80
    MAX_DIAMETER = 150
    MIN_FILLED_RATIO = 0.5
    
    def __init__(self, foldpath, filename):
        self.fname = filename
        self.folder = foldpath
        self.loadedImage = Image.open(foldpath + "/" + filename + ".jpg").convert('L')
        
    def labelize(self):
        edgeImage = self.imageEdges()
        segmentsImage = self.imageGeneticSegments(edgeImage)
        return self.imageLabels(segmentsImage)
        
    def imageEdges(self):
        im = numpy.array(self.loadedImage)
        
        #remove noise
        imGaus3 = ndimage.filters.gaussian_filter(im, 3)
        
        #edge detection
        imx = numpy.zeros(imGaus3.shape)
        ndimage.filters.sobel(imGaus3,1,imx)
        imy = numpy.zeros(imGaus3.shape)
        ndimage.filters.sobel(imGaus3,0,imy)
        edgeDetected = numpy.sqrt(imx**2+imy**2)
        return edgeDetected
    
    def imageSegments(self, edgeDetected):
        binaryImage = 1.0 * (edgeDetected > threshold_isodata(edgeDetected))
        dilated = dilation(binaryImage)
        filledImage = ndimage.binary_fill_holes(dilated)
        return filledImage
        
    def imageGeneticSegments(self, edgeDetected):
        binaryImage = 1.0 * (edgeDetected > self.THRESHOLD)
        dilated = dilation(binaryImage)
        filledImage = ndimage.binary_fill_holes(dilated)
        return filledImage
        
    def imageLabels(self, filledImage):
        labelImage = label(filledImage)
        image_label_overlay = label2rgb(labelImage, image=filledImage)
        return (labelImage, image_label_overlay)

    def drawLabels(self, labelImage, image_label_overlay):
        fig, ax = pylab.subplots(figsize=(10, 6))
        ax.imshow(image_label_overlay)
        for region in regionprops(labelImage):
            diameter = region.equivalent_diameter
            if diameter >= self.MIN_DIAMETER and diameter <= self.MAX_DIAMETER and region.extent >= self.MIN_FILLED_RATIO: 
                minr, minc, maxr, maxc = region.bbox
                rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                            fill=False, edgecolor='red', linewidth=2)
                ax.add_patch(rect)
        pylab.show()
    
    def writeProperties(self, labelImage, image_label_overlay):
        with open(self.fname + '.csv', 'w') as csvfile:
            fieldnames = ['object', 'filled area(pixels)', 'eq. diameter(pixels)', 'eccentricity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            counter = 0
            for region in regionprops(labelImage):
                diameter = region.equivalent_diameter
                if diameter >= self.MIN_DIAMETER and diameter <= self.MAX_DIAMETER and region.extent >= self.MIN_FILLED_RATIO: 
                    writer.writerow({'object': counter, 'filled area(pixels)': region.filled_area,
                                     'eq. diameter(pixels)': region.equivalent_diameter, 'eccentricity': region.eccentricity})
                    counter = counter + 1

#diff images --> general threshold
#recognizing cells --> tested
#incomplete cells --> region.extent
#fused cells?