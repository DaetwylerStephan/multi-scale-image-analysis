==============
Data stitching
==============

Our stitching pipeline
======================

Please first specify the folder path with the data to stitch and where you would like to save the new data:

.. code-block:: python

    experimentfolder_parent = "~/test_dataset/stitching" (your path)
    experimentfolder_result = experimentfolder_parent + "_stitched_test"


Next, determine a coarse positioning of the tiles using the physical coordinates of the microscope stage position
or using Fiji to determine the approximate overlay. Moreover, sometimes the fluorescent signal at the
edge of an image is weaker or absent. To remove this part of the image and also to reduce overall image size,
specify a cropping parameters.

.. code-block:: python

    #provide values for cropping.
    image_crops_y = [[640, 640 + 3276], [556, 456 + 3408], [452, 452 + 3796]]
    image_crops_x = [[400, 2500], [400, 2500], [400, 2500]]

    #provide expected displacement in (cropped) images.
    i_stitch.reference_displacement_x = [9, 6, 0]
    i_stitch.reference_displacement_y = [0, 2500, 4962]

Next, :meth:`multiScaleAnalysis.stitching.multiScale_stitching.image_stitcher.iterate_overfolder`
iterates over all folders of the experiment folder with the following structure:

.. code-block:: none

    .
    |-- experimentfolder_parent
    |   |-- t00000
    |   |   |-- low_stack000
    |   |   |   |--1_CH594_000000.tif
    |   |-- low_stack001
    |   |   |   |--1_CH594_000000.tif
    |   |-- low_stack002
    |   |   |   |--1_CH594_000000.tif

specified at the beginning of the script:

.. code-block:: python

    region = ["low_stack000", "low_stack001", "low_stack002"]
    sample = "fish1"
    channelnames = ["1_CH594_000000"]



The stitching class :meth:`multiScaleAnalysis.stitching.multiScale_stitching.image_stitcher` then
calculates the maximum intensity projections of each tile to reduce the computational workload.
Afterwards,  Fast Fourier transform-based cross-correlations on the overlapping sections of the background subtracted maximum intensity projections are calculated to obtain the translational shift between tiles as the highest value of all cross-correlations.
Lastly, the individual tiles are fused using a sigmoidal blending function. Alternatively, also fusion with maximum intensity projections is available.

Options:
--------
* Use_reference: The expected values for the whole time-lapse stitching might drift over time. If use_reference is set to 0,
  always start at each timepoint with the shift of timepoint-1. If use_reference is set to 1, resets the shift at every
  timepoint to the initially provided value.
* limit_search: Provide a narrow search window to tune for the best overlap of the stitching process.
* optimize_alignment: If set to 1, optimize the shift values at every timepoint, e.g. if there is sample movement.


Output
======

The output of the pipeline then produces the following folders and files:

.. code-block:: none

    .
    |-- experimentfolder_parent_stitched
    |   |-- fish1
    |   |   |-- t00000
    |   |   |   |--1_CH594_000000.tif
    |   |-- fish1_max
    |   |   |   |--1_CH594_000000
    |   |   |   |  |--t00000.tif
    |   |-- fish1_max_side
    |   |   |   |--1_CH594_000000
    |   |   |   |  |--t00000.tif

Here, "fish1" is the sample (as defined above) and the stitched 3D stacks are saved in the "fish1" folder. The maximum intensity projection
of the stitched 3D data set are saved in the "fish1_max" folder and the side view (xz) maximum intensity projections for quick data visualization.

Test dataset
============

To test the stitching code, we provide a test data set of an entire zebrafish embryo with labelled
vaculature, *Tg(kdrl:rasCherry)*, consisting of
one timepoint (t00000) and three regions (low_stack000, low_stack001, low_stack002)
imaged with the low-resolution light-sheet modality.

To download the dataset, please download the folder Exemplary_StitchingDataset:

on Synapse https://doi.org/10.7303/syn61795850
or Zenodo: https://doi.org/10.5281/zenodo.12791724


Alternatives
============

A well tested and established open-source alternative for stitching is BigStitcher:
https://imagej.net/plugins/bigstitcher/

Alternatively, also the PetaKit5D software tools might be helpful:
https://github.com/abcucberkeley/PetaKit5D
