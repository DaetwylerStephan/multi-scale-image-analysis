.. _lowressegmentation:

===========================
Low-resolution segmentation
===========================

To quickly segment the low-resolution data, we leverage GPU-accelerated
`Pyclesperanto_prototype <https://github.com/clEsperanto/pyclesperanto_prototype>`_.
Conveniently, a Napari plugin called `napari-pyclesperanto-assistant <https://clesperanto.github.io/napari_pyclesperanto_assistant>`_ is
available to optimize the segmentation pipeline.

Setting up segmentation
=======================

Specifically, we initialize the segmentation by setting the path to the data, where to save it and which channels to segment:

.. code-block:: python

    parentfolder = '~/test_dataset/low_resSegmentation/fish1'
    resultsfolder = parentfolder + "_segmented"
    channellist = ['1_CH488_000000', '1_CH552_000000']

It then iterates over a folder with the following structure:

.. code-block:: none

    .
    |-- parentfolder
    |   |-- t00000
    |   |   |-- 1_CH488_000000.tif
    |   |   |-- 1_CH552_000000.tif
    ...

Output
======

It generates the segmentation labels and saves them as .tif files (8-bit or 16-bit, depending on the
number of labels). Moreover, it saves the label statistics in an Excel document per timepoint.

.. code-block:: none

    .
    |-- parentfolder
    |   |-- t00000
    |   |   |-- 1_CH488_000000.tif
    |   |   |-- 1_CH552_000000.tif
    |-- parentfolder_segmented
    |   |-- 1_CH488_000000
    |   |   |-- t00000
    |   |   |   |-- 1_CH488_000000sg.tif
    |   |-- 1_CH552_000000
    |   |   |-- t00000
    |   |   |   |-- 1_CH552_000000sg.tif
    |-- parentfolder_segmented_xlsx
    |   |-- 1_CH488_000000
    |   |   |-- t00000.xlsx
    |   |-- 1_CH552_000000
    |   |   |-- t00000.xlsx
    ...

Test data for low-resolution visualization
==========================================

Test data is available for the low-resolution visualization  in the folder Exemplary_Segmentation/low_resolution.

:on Synapse: https://doi.org/10.7303/syn61795850
:or Zenodo: https://doi.org/10.5281/zenodo.12791724

