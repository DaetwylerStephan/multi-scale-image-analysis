===========================
Cell Shape Feature Analysis
===========================

Cell shape feature analysis performs classification of global morphological cell shape
features for cell classification. This analysis pipeline was first pioneered and described
in our paper "In vivo 3D profiling of site-specific human cancer cell morphotypes in zebrafish"
(`Link to paper <https://doi.org/10.1083/jcb.202109100>`_) and applied here to identify
changes in morphology over hours of imaging and during macrophage-cancer cell interactions.

The pipeline calculates 12 global morphological shape feature for classification:
volume, surface area, solidity, sphericity, longest length, extend, aspect ratio, roughness,
volume sphericity, radius sphericity, ratio sphericity, and circumscribed sphere area ratio.

These feature span a space which is reduced through PCA analysis to two dimensions for visualization.

To run the script, the data should be in the following format:

.. code-block:: none

    .
    |-- TimeSeries
    |   |-- t00000
    |   |   |-- Cell1
    |   |   |   |--segmentedImage.tif
    |   |   |-- Cell2
    |   |   |   |--segmentedImage.tif
            ...
    |   |-- t00001
    |   |   |-- Cell1
    |   |   |   |--segmentedImage.tif
    |   |   |-- Cell2
    |   |   |   |--segmentedImage.tif
            ...

Running the Matlab code
=======================

If you run the Matlab, please first add the Matlab folder Highres_curvature to your active
`Matlab search path <https://www.mathworks.com/help/matlab/ref/addpath.html>`_. Next,




Matlab compiled version
=======================

If you do not have access to Matlab, we provide a compiled version of the code as ".exe" file.
To run it, please double click on the compiled version and follow the installation instructions.
In the installation process also a `Matlab runtime <https://www.mathworks.com/products/compiler/matlab-runtime.html>`_
environment is installed to run the code. After installation, the compile code is ready to run.
When prompted, please provide the path to the folder with all the timepoint paths (e.g. TimeSeries folder above).


Output:

The Matlab script will produce several outputs and save them in the data folder as follows:

.. code-block:: none

    .
    |-- TimeSeries
    |   |-- Results
    |   |   |-- data_pcSpace.png
    |   |   |-- FeatureSpace_pcSpace.png
    |   |   |-- highResResults_geoTable.xlsx
    |   |   |-- highResResults_pca.xlsx
    |   |   |-- highResResults_pvalue.xlsx
    |   |   |-- PC_contribution.png
    |   |   |-- PvalueMatrix.png

The "data_pcSpace.png" contains a plot of the position of all cells in the PCA space. To visualize,
which components contribute to the principal components, the biplot (FeatureSpace_pcSpace.png)
is saved as well in the Results folder.

The analysis of the cell shapes is further saved in tabular format in the highResResults_geoTable.xlsx, where all
values of the global morphological geometric feature analysis are saved (for each cell). The highResResults_pvalue.xlsx
then contains the coordinates of each of these cells in the principal component space. The
highResResults_pvalue.xlsx file then contains the p-value of comparing the shapes of both cell distributions in both
top folders (timepoints / conditions etc).

Lastly, the PC_contribution.png file describes the variability in the data explained by each principal
component and the PvalueMatrix.png highlights how similar both conditions (or timepoints) are.



Test data for cell shape feature analysis
=========================================

Test data is available for the cell shape feature analysis on Synapse in the folder
Code_Example_Datasets/Exemplary_ShapeFeatureAnalysis:

LINK

It contains a folder to a collection of cells from two timepoints.
