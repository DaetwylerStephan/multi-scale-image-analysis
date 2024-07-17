===========================
Hopkins Statistics Analysis
===========================

To analyze the distribution of macrophages over time in an entire zebrafish larvae,
we applied the `Hopkins statistics <https://journal.r-project.org/articles/RJ-2022-055/>`_.
A high value of the Hopkins statistics H indicates indicates that the underlying data shows a high cluster tendency, e.g. H>0.75
indicates a cluster tendency at the 90% confidence level.

Zebrafish volume approximation
==============================

The Hopkins statistics requires the simulation of random points. To do this, we obtained
the 3D zebrafish volume V as a space for possible locations of macrophages to
compare the observed spatial distribution (real positions) against randomly
generated distributions (random positions).

To run the ImageJ macro, drag and drop the generate_fish_outline_forSegmentation_percentile.ijm
file into Fiji and modify the imagename, parentfolder (where all timepoints are saved),
savefolder (where to save the 3D stacks with the volume) and savefolder_max (where the maximum intensity
projections of the 3D stacks) are saved..

.. code-block:: java

    imagename = "1_CH594_000000.tif"
    parentfolder= "~/fish1"
    savefolder= "~/fish_volume"
    savefolder_max= "~/fish_volume_max"

Hopkins statistics calculation
==============================

Next, a Matlab script enables calculation of the Hopkins statistic. It requires a
list of position of real macrophage positions in an Excel file (t0000.xlsx) and
an image with a binary mask for the volume to simulate random positions (fishvolume_t00000.tif).

.. code-block:: none

    .
    |-- TimeSeries
    |   |-- t00000
    |   |   |-- fishvolume_t00000.tif
    |   |   |-- t00000.xlsx
            ...

To modify the Matlab script, ....

Matlab compiled version
=======================

If you do not have access to Matlab, we provide a compiled version of the code as ".exe" file.
To run it, please double click on the compiled version and follow the installation instructions.
In the installation process also a `Matlab runtime <https://www.mathworks.com/products/compiler/matlab-runtime.html>`_
environment is installed to run the code. After installation, the compile code is ready to run.

Test data for cell shape feature analysis
=========================================

Test data is available for the cell shape feature analysis on Synapse in the folder
Code_Example_Datasets/Exemplary_ShapeFeatureAnalysis:

LINK

It contains a folder to a collection of cells from two timepoints.







