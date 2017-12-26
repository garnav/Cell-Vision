# Cell Vision
A tiny program that extracts the number, area and eccentricity of microscopic cells from high resolution images.

This project was conceived to aid Grad Maria Modanu quickly analyze over 10,000 nematode sperm cell images.

## Features
To identify these properties, each image undergoes the following steps:

**Gaussian Noise Removal -> Sobel Edge Detection -> Thresholding -> Dilation -> Segmentation -> Labelling**

### Example - Single Image
| True Image | Labelled Image |
| ---------- | -------------- |
| <img src="https://github.com/garnav/Cell-Vision/blob/master/images/DSC_0102_original.JPG" width="600"> | <img src="https://github.com/garnav/Cell-Vision/blob/master/images/DSC_0102.png" width="600"> |

### Example - Single Cell
| True Cell | Post Thresholding | Post Labelling |
| --------- | ----------------- | -------------- |
| <img src="https://github.com/garnav/Cell-Vision/blob/master/images/actual_cell.png" width="300"> | <img src="https://github.com/garnav/Cell-Vision/blob/master/images/general_threshold_cell.png" width="300"> | <img src="https://github.com/garnav/Cell-Vision/blob/master/images/segmented_cell.png" width="300"> |

## Design Choices

### Thresholding
Instead of choosing a threshold based on the given image, a constant threshold is used for every image. An analysis of over 100 images tested using both techniques reveals that using a constant threshold results in more cells recognized per image and fewer non-cell structures filled-in post segmentation. An example of these differences is shown below:

| Constant Threshold (= 15.0) | Histogram Based Threshold (ISODATA) |
| --------------------------- | ----------------------------------- |
| <img src="https://github.com/garnav/Cell-Vision/blob/master/images/label_thresholdgeneral.png" width="600"> | <img src="https://github.com/garnav/Cell-Vision/blob/master/images/label_thresholdofimage.png" width="600"> |

### Segmentation & Labelling
To avoid labelling noise in the image as cells, the program relies on two techniques:
* **Min. & Max. Diameter** : All cells are between 80 and 150 pixels in diameter. Any objects that don't fit into this size range are eliminated.
* **Percentage Filled-In Region** : Regions of bright segments are highlighted using skimage. Each region is identified using a rectangular box. However, unfilled cells and noise segments have a lower **filled to total area ratio** than true cells. Thus, we only highlight those segments whose filled area ratio is above a constant value. An example of these differences is shown below:

| Without A Filled Area Threshold | With a Filled Are Threshold |
| ------------------------------- | --------------------------- |
| <img src="https://github.com/garnav/Cell-Vision/blob/master/images/restricted_labelling.png" width="600"> | <img src="https://github.com/garnav/Cell-Vision/blob/master/images/restricted_labelling_withpercentage.png" width="600"> |

## Known Issues

### Unfilled Cells
The program relies on the slightly different tint of cell membranes to correctly outline cells. However, due to noise created by other substances in the solution during imaging, this does not always clearly separate the membrane from the image's background. Consequently, during edge detection, only part of the membrane is recognized as the cell's 'edge' and these show up as unfilled cells during segmentation.

### Fused Cells
Before segmentation, the program uses dilation to paper over some cracks in the cell's edges. Unfortunately, this sometimes causes the outline of two adjacent cells to overlap, resulting in a single fused structure as opposed to two separate cells.

| Unfilled Cells | Fused Cells |
| -------------- | ----------- |
| <img src="https://github.com/garnav/Cell-Vision/blob/master/images/not_cell_boxed.JPG" width="200"> | <img src="https://github.com/garnav/Cell-Vision/blob/master/images/two_cells_unboxed.JPG" width="200"> |

## Contributors
* Arnav Ghosh (ag983)
