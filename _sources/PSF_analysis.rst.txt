============
PSF analysis
============



Running the Python script
=========================

To run the PSF script, first set the file paths to the image stack and where to save the results.
The imagefilepath is the file containing the image stack with the beads (raw image). The output of the script
produces an Excel file with all identified beads and their PSF values (imagefilepath_Excelfile), a summary
statement with the median PSF values in a text file (imagefilepath_textfile), a plot of the PSF values
along the image dimensions (imagefilepath_plot) and for trouble-shooting, all identified beads and labels
can be saved (imagefilepath_labelled).

.. code-block:: python

    # generate file paths
    parentfolder = "~/beadfolder/"
    imagefilepath = parentfolder + "1_CH488_000000.tif"  # rawimage name
    imagefilepath_labelled = parentfolder + "1_CH488_000000labelled.tif"  # save image with labelled bead positions
    imagefilepath_plot = parentfolder + "psf_plot.jpg"  # plot bead profiles along image/stack axis
    imagefilepath_Excelfile = parentfolder + "psf_values.xlsx"  # save bead positions and their values to Excel file
    imagefilepath_textfile = parentfolder + "psf_values.txt"  # save summary textfile

Next, define parameters used for calculation of the PSFs:

.. code-block:: python

    # parameters
    threshold = 500
    areacutoff = 300
    lateral_dist = 10
    axial_dist = 6
    pixelvalue_lateral_um = 0.117
    pixelvalue_axial_um = 0.2
    cutoff_lateralPSFvalue = 1
    cutoff_axialPSFvalue = 2
    showbeadplot = True

Parameter explanation:
In the script, beads are identified as pixels with an intensity higher
than a threshold (threshold). Subsequent connected component labeling identifies the centroid of
these beads. The obtained list of centroids is filtered for beads too close to the edge and for beads
(large clusters/aggregates), that exceed a defined value in area (areacutoff).

To calculate the point spread function (PSF) for a bead, an image with a single bead in it is required.
For this, the image stack is cropped around the centroid of the selected bead with
[x +/- lateral_dis, y +/- lateral_dis, z +/- axial_dist].
There are two distances here as the axial PSF value is often larger than the lateral PSF value.
To translate the pixel measurements to physical distances, it is required to calibrate the measurement
with the physical sizes of each pixel (e.g. in micrometer) for lateral (pixelvalue_lateral_um) and
axial (pixelvalue_lateral_um) directions. As preparation of bead samples often leads to aggregates,
a maximally expected value of the PSF (in physical distances) can be chosen to exclude these aggregates
from the visualization and median calculation (cutoff_lateralPSFvalue, cutoff_axialPSFvalue). To show
the resulting plot of PSF values along the image directions while running the script, select: showbeadplot = True

To run the script after changing the parameters, use the terminal with the activated conda environment (see Installation),
navigate to the folder and enter:

.. code-block:: console

   (imageanalysis_env) ~/Tools$  python PSF_measurements.py


Note: The calculation of the PSF follows the recipe of the well-used MetroloJ plugin:
https://imagejdocu.list.lu/plugin/analysis/metroloj/start

Testdata set for PSF characterization
=====================================

A test data set is available on Synapse to calculate the PSF values of an example bead sample from the
high-resolution axially-swept light-sheet acquisition.

Synapse link: LINK