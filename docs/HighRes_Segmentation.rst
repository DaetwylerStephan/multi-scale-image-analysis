============================
High-resolution segmentation
============================

For high-resolution segmentation of our data, we rely on `u-Segment3D <https://github.com/DanuserLab/u-segment3D>`_.
U-Segment3D is a 3D segmentation pipeline for 3D data that aggregates 2D `Cellpose <https://cellpose.readthedocs.io/en/latest/>`_ segmentations
in three dimensions into a consistent 3D segmentation.

.. note::
    As the data in our paper was relying on an early
    version of u-Segment3D, we would like to guide the user to the latest version of
    the software https://github.com/DanuserLab/u-segment3D for future use and `tutorials
    <https://github.com/DanuserLab/u-segment3D/tree/master/tutorials>`_.

A preprint is available here that describes in detail the technological and computational
innovations in this novel segmentation approach:
https://www.biorxiv.org/content/10.1101/2024.05.03.592249v2

Our pipeline
------------

The here provided code, however, helps the reader to understand the step-by-step scripts
run to obtain the segmentation described in our manuscript:

:meth:`multiScaleAnalysis.SegmentationHighres.ConnectedComponent_MacrophageSegmentation`.
First, we pre-processed the data with (optional) registration using PyStackReg, background
smoothing, normalization, and Wiener-Hunt deconvolution (scikit-image). Then, we
segmented the high-resolution data using multi-otsu thresholding (scikit-image libary)
and subsequently labelled connected components. This approach worked well
for single, protrusive macrophages.

:meth:`multiScaleAnalysis.SegmentationHighres.postprocessing_removeCancersignal`.
To clean up the macrophage segmentation (bleed-through from the cancer cells), we
removed the cancer cell signal from the images.

:meth:`multiScaleAnalysis.SegmentationHighres.Cellpose_based_MacrophageSegmentation`.
Next, we realized that touching macrophages were not distinguished well in the
multi-otsu thresholding and connected component approach. Therefore, we applied
deep learning based segmentation using `Cellpose <https://cellpose.readthedocs.io/en/latest/>`_ (cytoplasm
2.0 model/cyto2). With Cellpose, we computed segmentations slice-by-slice
in x-y, x-z, y-z views, and aggregated the resulting 2D segmentation into a
single consensus 3D segmentation using `u-Segment3D <https://github.com/DanuserLab/u-segment3D>`_.

:meth:`multiScaleAnalysis.SegmentationHighres.Merge_ConnectedComponents_Cellpose`.
To successfully merge both segmentations, we leveraged that touching macrophages
exceeded a defined volume threshold (40000 voxels - based on histogram distribution in the control data).
Based on this, we replaced large segmented cell clusters with labels of the Cellpose-based
segmentation and post-processed the merged segmentation by merging labels below a
5000 voxels threshold.

:meth:`multiScaleAnalysis.SegmentationHighres.Manual_curation`
Lastly, we performed manual curation of the dataset, supported by a custom Python
script.

