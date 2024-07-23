==================
Data visualization
==================

Here we provide tools to visualize tens to hundreds of timepoints of large light-sheet
microscopy data in 3D. For this, we leverage the open-source python based Napari software
https://napari.org/stable/.

Generate a custom colormap for labels
=====================================

To visualize the segmented data with a dedicated colormap from Fiji (Rainbow Smooth.lut), we
designed our own Fiji/ImageJ macro to save the data in the appropriate format for Napari.

To install the Rainbow Smooth.lut, go to File>Import>Lut.. and select the Rainbow Smooth.lut from
the folder.

To run the ImageJ macro, drag and drop the ijm file into Fiji and modify the path and segmentedfilename to the data.

.. code-block:: java

    parentpath = "Z:/Fiolka/LabMembers/Stephan/multiscale_data/revision_experiments/test_dataset/visualization";
    segmentedfilename = "filename"

The data should be in the following format:

.. code-block:: none

    .
    |-- parentpath
    |   |-- t00000
    |   |   |-- filename.tif
    |   |-- t00001
    |   |   |-- filename.tif
    ...

It will produce the following output in the same folder:

.. code-block:: none

    .
    |-- parentpath
    |   |-- t00000
    |   |   |-- filename.tif
    |   |   |-- filename_red.tif
    |   |   |-- filename_green.tif
    |   |   |-- filename_blue.tif
    |   |-- t00001
    |   |   |-- filename.tif
    |   |   |-- filename_red.tif
    |   |   |-- filename_green.tif
    |   |   |-- filename_blue.tif
    ...

with filename_red.tif, filename_green.tif, filename_blue.tif containing
the red, green and blue contributions of the RGB labels. These individual label images can then
be loaded to napari to make label the individual segmented cells in different colors.

Visualization of low-resolution data
====================================

To iterate over a folder of raw images and segmentations, we scripted 3D rendering
with Napari to obtain consistent renderings at different timepoints with the same parameters.

An example script for low-resolution visualization is available under visualize_stitched_lowres.py
:meth:`multiScaleAnalysis.visualization.visualize_stitched_lowres`

To run it, provide the data paths to the low-resolution rawdatafolder, the low-resolution segmented data and
where you want to save the rendered data (imagevisu.visualizedfolder).

.. code-block:: python

    imagevisu.rawdatafolder = os.path.join(rawdatafolder_parent, "rawdata")
    # segmented data
    imagevisu.segmentationfolder = os.path.join(rawdatafolder_parent, "lowres_segmentation_labelimages")
    imagevisu.visualizedfolder = imagevisu.rawdatafolder + "_visualized"


Then, the scripts iterates over the individual timepoints with the visualization parameters defined by
a visualization_param dictionary:

.. code-block:: python

    visualization_param = dict(
        camera_angle1 = (169, -18, 72),
        camera_angle2 = (18, -53, -120),
        camera_zoom=0.7,
        raw_contrast_limits=(300, 1400),
        raw_contrast_limits_vessels=(600, 15027),
        raw_gamma=0.9,
        raw_gamma_vessel=0.5,
        label_opacity=0.51,
        rendering_dimension=3,
        blending1='translucent',
        blending2='additive',
        establish_param=0,
        scale_to_save=5
    )


Here, we generate and save two camera angles (camera_angle1, camera_angle2), set the zoom (camera_zoom),
the contrast limits of both raw data channels (raw_contrast_limits,raw_contrast_limits_vessels), the
gamma values of both raw data channels (raw_gamma, raw_gamma_vessel), define that the data is rendered in 3D
(rendering_dimension), label opacity (label_opacity), two blending modes based on the data to add (blending1, blending2),
and the quality of the saved rendering (scale_to_save).

Note 1: If you don't know what parameters such as contrast limits or angles to use, set the establish_param flag to 1
and the script will open Napari with the images to find the best parameters. For batch processing, set establish_param=0.

Note 2: We downsampled the rawimages to provide more efficient computation to fit the label image.

Test data for low-resolution visualization
==========================================

Test data is available for the low-resolution visualization in the folder Exemplary_VisualizationDataset.

on Synapse https://doi.org/10.7303/syn61795850
or Zenodo: https://doi.org/10.5281/zenodo.12791724

It contains data in the folder structured as:

:low_resolution_rawdata: The raw data to visualize (macrophage and vessels)
:low_resolutionsegmentation: The low-resolution segmentation to visualize
:low_resolutionsegmentation_labelimages: The low-resolution segmentation after the ImageJ macro
:low_resolution_visualization_results: The final visualization results.

Visualization of high-resolution data
=====================================

High-resolution data can be visualized similarly as low-resolution data. Here, we describe
in more detail the visualization of high-resolution rawdata of cancer spheroids in a collagen matrix
from SUM159 breast cancer cells labelled with two colors 1:1 (Lifeact-GFP and the Lifeact-mCherry).
The python file for this script is in :meth:`visualize_with_napariHighRes_spheroids.py`.

First, specify the path to the raw data (imagevisu.rawdatafolder), the folder to save the rendering results
(imagevisu.visualizedfolder), the region to visualize (imagevisu.region).

Moreover, if you already have established the visualization parameters, choose establish_param=0. If not,
set establish_param=1, which will open Napari at timepoint zero to establish the rendering parameters.

.. code-block:: python

    imagevisu.rawdatafolder = '~/test_dataset/visualization_highres'
    experimentfolder_result = imagevisu.rawdatafolder + "_highres_visualized_test"
    imagevisu.visualizedfolder = os.path.join(experimentfolder_result, 'visualized')
    imagevisu.region = 'high_stack_002'
    imagevisu.establish_param = 0

In this example, we set the visualization parameters as follows:

.. code-block:: python

    visualization_param = dict(
        camera_angle1=(9.008, -20.465, 63.542),
        camera_angle2=(14.71, -37.523, 70.406),
        camera_zoom=0.28,
        raw_contrast_limits_magenta=(78, 480),
        raw_contrast_limits_cyan=(77, 1463),
        raw_gamma_magenta=0.60,
        raw_gamma_cyan=0.96,
        magenta_colormap ='magenta',
        cyan_colormap='cyan',
        opacity_cyan=0.64,
        rendering_dimension=3,
        raw_rescale_factor =[2.564, 1, 1],
        scale_to_save=5,
        imagename_cyan="1_CH488_000000.tif",
        imagename_magenta="1_CH594_000000.tif"
    )

Specifically, we generate and save two camera angles (camera_angle1, camera_angle2), set the zoom (camera_zoom),
the contrast limits of both raw data channels (raw_contrast_limits_magenta,raw_contrast_limits_cyan), the
gamma values of both raw data channels (raw_gamma_magenta, raw_gamma_cyan),
set the colormaps (magenta_colormap, opacity_cyan), define the opacity of the image on top (opacity_cyan), define that the data is rendered in 3D
(rendering_dimension), set the voxel spacings as the data is not isotropic (raw_rescale_factor), the quality of the saved rendering (scale_to_save),
and the two names of the raw data images (imagename_cyan, imagename_magenta).

In addition to the here described script for rendering spheroids, we also provide scripts used to
visualize A375 cancer cells, MDA-MB-231 cancer cells, nuclei histones, and U-2 OS cancer cells with
segmented macrophages.


Test data for high-resolution visualization
===========================================

Test data is available for the high-resolution visualization in the folder
Exemplary_VisualizationDataset.

:on Synapse: https://doi.org/10.7303/syn61795850
:or Zenodo: https://doi.org/10.5281/zenodo.12791724

It contains:

:high_resolution_rawdata: The raw data to visualize (two spheroid channels)
:high_resolution_visualization_results: The final visualization results.


