=======================
Cell Curvature Analysis
=======================

Cell curvature is an important morphological feature of cell shape and involved
in organizing cell signaling (e.g. through `Septin localization <https://www.pnas.org/doi/full/10.1073/pnas.2208253120>`_.

To measure and visualize cell curvature, we developed custom Matlab code
that takes a binary cell segmentation mask and generates a collada (.dae) file.
The collada file format can be easily imported into Chimera
for Visualization: https://www.cgl.ucsf.edu/chimera/.







Matlab compiled version
=======================

If you do not have access to Matlab, we provide a compiled version of the code as ".exe" file.
To run it, please double click on the compiled version and follow the installation instructions.
In the installation process also a `Matlab runtime <https://www.mathworks.com/products/compiler/matlab-runtime.html>`_
environment is installed to run the code. After installation, the compile code is ready to run.


Test data for cell curvature analysis
=====================================

Test data is available for the cell shape feature analysis on Synapse in the folder
Code_Example_Datasets/Exemplary_CurvatureAnalysis:

LINK

It contains a segmented cells to visualize.