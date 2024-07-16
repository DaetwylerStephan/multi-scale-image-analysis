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

Next, a Matlab script enables calculation of the Hopkins statistic:


Matlab compiled version
=======================

If you do not have access to Matlab, we provide a compiled version of the code:





