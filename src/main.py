# main.py
# Arnav Ghosh
# 7th June 2017

import os
from analysis import Analysis

INPUT_LOC = "inputs"
PROP_LOC = "output"
LABELS_LOC = "labels"

#iterate over images and save their properties
def main():
	createDirs()
	batchAnalyze()

def batchAnalyze():
	files = os.listdir(os.path.join(os.pardir,INPUT_LOC))
	for imagefile in files:
		imageAnalysis = Analysis(os.path.abspath(os.path.join(os.pardir,INPUT_LOC)), imagefile)
		labelImage, imageOverlay = imageAnalysis.labelize()
		imageAnalysis.drawLabels(labelImage, imageOverlay, os.path.join(os.pardir,LABELS_LOC))
		imageAnalysis.writeProperties(labelImage, imageOverlay, os.path.join(os.pardir,PROP_LOC))

def createDirs():
	try:
		os.mkdir(os.path.join(os.pardir,PROP_LOC))
		os.mkdir(os.path.join(os.pardir,LABELS_LOC))
	except OSError:
		pass