# Self-driving, multi-scale imaging

This repository contains the software to analyze data from a self-driving, multi-scale microscope and tools to process and analyse the resulting data.

A preprint about this work is available:
https://www.biorxiv.org/content/10.1101/2024.02.28.582579v1

and detailed documentation is available here: 
https://daetwylerstephan.github.io/multi-scale-image-analysis/

including links to testdata sets and parameters.

As a quick overview:

### Highres_curvature
Contains code to determine the curvature of cells such as macrophages from the high-resolution data, including a compiled Matlab runtime version.

### Highres_morphologicalFeatures
Contains code to run the morphological feature analysis of cells in the high-resolution data, including a compiled Matlab runtime version.

### HopkinsStatistics_Lowres
Contains code to calculate the Hopkins statistics based on the low-resolution cell position data, including a compiled Matlab runtime version.

### SegmentationHighres
Contains code to run our high-resolution macrophage segmentation pipeline using connected component labeling and a Cellpose-based 3D segmentation pipeline.

### SegmentationLowres
Contains code to run our low-resolution macrophage segmentation pipeline based on CLIJ.

### Stitching
Contains code to stitch 3D data using translation based on the stage positions using Fast Fourier transform-based cross-correlations on the overlapping sections.

### Visualization
Contains code to visualize time-lapse data using ImageJ (generatelabel_colormap.ijm) and Napari (low- and high-res data).
