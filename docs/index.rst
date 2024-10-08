.. multiScaleAnalysis documentation master file, created by
   sphinx-quickstart on Tue Jul  9 17:17:32 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Self-driving, multi-scale image analysis
========================================

**Self-driving, multi-scale image analysis software** is an open-source collection of Python
and Matlab code to analyse custom multi-scale light-sheet microscope data
from continuous, long-term, simultaneous low- and high-resolution imaging.

If you use this code, please cite our preprint:
"Imaging of cellular dynamics *in vitro* and *in situ*: from a whole organism to sub-cellular imaging with self-driving, multi-scale microscopy"
by Stephan Daetwyler, Hanieh Mazloom-Farsibaf, Felix Y. Zhou, Dagan Segal,
Etai Sapoznik, Jill M. Westcott, Rolf A. Brekken, Gaudenz Danuser and Reto Fiolka
https://www.biorxiv.org/content/10.1101/2024.02.28.582579v1

The Github repository for all the described code is here:
https://github.com/DaetwylerStephan/multi-scale-image-analysis/

Test data to run the scripts is available on Synapse https://doi.org/10.7303/syn61795850
and Zenodo: https://doi.org/10.5281/zenodo.12791724

.. toctree::
   :caption: Getting started and installation
   :maxdepth: 2

   Installation

.. toctree::
   :caption: Microscope characterization
   :maxdepth: 2

   PSF_analysis
   ShannonEntropyAnalysis

.. toctree::
   :caption: Low-resolution analysis
   :maxdepth: 2

   Data_stitching
   LowRes_Segmentation
   HopkinsStatistics

.. toctree::
   :caption: High-resolution analysis

   HighRes_Segmentation
   Cell_ShapeAnalysis
   Cell_CurvatureAnalysis

.. toctree::
   :caption: Data visualization

   Data_visualization

.. toctree::
   :caption: Python API references
   :maxdepth: 1

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`