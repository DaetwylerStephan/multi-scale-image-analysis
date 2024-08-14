===========================
Cell Shape Feature Analysis
===========================

Cell shape feature analysis performs classification of global morphological cell shape
features for cell classification (Manuscript Figure 3). This analysis pipeline was first pioneered and described
in our paper "In vivo 3D profiling of site-specific human cancer cell morphotypes in zebrafish"
(`Link to paper <https://doi.org/10.1083/jcb.202109100>`_) and applied here to identify
changes in morphology over hours of imaging and during macrophage-cancer cell interactions.

The pipeline calculates 12 global morphological shape features for classification:
volume, surface area, solidity, sphericity, longest length, extend, aspect ratio, roughness,
volume sphericity, radius sphericity, ratio sphericity, and circumscribed sphere area ratio.

These features span a space which is reduced through PCA analysis to two dimensions for
analysis (how similar are two cell populations, e.g. at different conditions or time)
and visualization.

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


If you run the Matlab code, first clone the Github repository and set Matlab's path to
include all the Matlab functions provided by
the ``Highres_morphologicalFeatures``  package on the GitHub repository,
using the `Set Path <https://www.mathworks.com/help/matlab/matlab_env/add-remove-or-reorder-folders-on-the-search-path.html>`_
button in Matlab (Home > Environment > Set Path> Add with subfolders).

To run the cell shape feature analysis, open ``runGlobalFeatureAnalysis_US2O.m`` by typing "edit runGlobalFeatureAnalysis_US2O"
in Matlab's command window. ``runGlobalFeatureAnalysis_US2O.m`` is the main run script that
analyzes and compares cell shape features over the entire experiment. In this script, revise
the "imageDirectory" for loading the data and "saveDirectory"
for saving the results. Save the changes and run the function by typing runGlobalFeatureAnalysis_US2O
in Matlab's command window.


Matlab compiled version
=======================

If you do not have access to Matlab, we provide a compiled version of the code as ".exe" file.
To run it, please double click on the compiled version and follow the installation instructions.
In the installation process also a `Matlab runtime <https://www.mathworks.com/products/compiler/matlab-runtime.html>`_
environment is installed to run the code. After installation, the compiled code is ready to run.
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

Test data is available for the cell shape feature analysis in the folder
Code_Example_Datasets/Exemplary_ShapeFeatureAnalysis:

:on Synapse: https://doi.org/10.7303/syn61795850
:or Zenodo: https://doi.org/10.5281/zenodo.12791724

It contains a folder to a collection of macrophages (cells) from two timepoints in a zebrafish
xenograft model.
