========================
Shannon Entropy Analysis
========================

Running the Python script
=========================

To run the script, please provide the filenames where the data is saved (parentfolder) and where the
Excel file with the Shannon Entropy values should be saved.

.. code-block:: python

    parentfolder = "~/timeseriesfolder"
    result_xlsxfile = "~/analysis/ShannonEntropyValues.xlsx"

The data in the parentfolder should be organized in the following way:

.. code-block:: none

    .
    |-- timeseriesfolder
    |   |-- t00000.tif
    |   |-- t00001.tif
    |   |-- t00002.tif
    |   |-- t00003.tif
    ....

Output
======

The script will generate a plot of the Shannon Entropy values over time and save the data as an Excel file.


Testdata set for PSF characterization
=====================================

Test data is available for the calculating the Shannon Entropy of bead images
in the folder Exemplary_ShannonEntropy/timeseries.

:on Synapse: https://doi.org/10.7303/syn61795850
:or Zenodo: https://doi.org/10.5281/zenodo.12791724
