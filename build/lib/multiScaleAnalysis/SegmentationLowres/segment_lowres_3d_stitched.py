
import pyclesperanto_prototype as cle
from tifffile import imread, imwrite
import os
import pandas as pd
import scipy.ndimage as ndimage

import numpy as np

print(cle.cl_info())

class segment_macrophage_lowres_class():
    """
    This class gathers all functions to segment the macrophage and cancer cells of the low-resolution data.
    """

    def __init__(self):
        """
        Initialization, including GPU initalization and parameter
        """
        #1. initialize GPU-------------------------------------
        gpu_devices = cle.available_device_names(dev_type="gpu")
        print("Available GPU OpenCL devices:" + str(gpu_devices))

        # selecting an Nvidia RTX
        cle.select_device("RTX")
        print("Using OpenCL device " + cle.get_device().name)
        self.image_tosegment = []
        self.lateral_axialratio = 3.5/0.38


    def open_image(self, imagename):
        """
        Open image.

        :param imagename: file path to current image
        """
        self.image_tosegment = imread(imagename)

    def segment_macrophage(self, savepath, background_substracted_path="path", savepath_xlsx="pathxlsx"):
        """
        Segment macrophages in the low-resolution image and save the resulting segmentation and segmentation statistics.

        :param savepath: path to save segmentation outcome
        :param background_substracted_path: path to save background substracted image (optional)
        :param savepath_xlsx:  path to save segmentation statistics
        """
        #downsample 3D volume so that it can be handled by GPU.
        im_rescaled = ndimage.zoom(self.image_tosegment, [1., 1. / self.lateral_axialratio, 1. / self.lateral_axialratio], order=1, mode='reflect')
        input_gpu = cle.push(im_rescaled)

        #pre-processing data
        background_subtracted = cle.top_hat_box(input_gpu, radius_x=6, radius_y=6, radius_z=6)
        if background_substracted_path != "path":
            imwrite(background_substracted_path, background_subtracted)
        print("background calculated")

        #thresholding and voronoi otsu labeling
        image1_t = cle.greater_constant(background_subtracted, None, 88.0)
        segmented = cle.voronoi_otsu_labeling(image1_t, None, 2.0, 1.0)
        segmented_withoutsmalllabels = cle.exclude_small_labels(segmented, maximum_size=10.0)

        segmented_array = cle.pull(segmented_withoutsmalllabels)

        #get segmentation statistics
        statistics = cle.statistics_of_labelled_pixels(input_gpu, segmented_array)
        table = pd.DataFrame(statistics)
        print("nb rows:" + str(table.shape[0]))
        if table.shape[0]<256:
            imwrite(savepath, segmented_array.astype("uint8"))
        else:
            imwrite(savepath, segmented_array.astype("uint16"))

        if savepath_xlsx != "pathxlsx":
            table.to_excel(savepath_xlsx)

    def segment_cancercells(self, savepath, background_substracted_path="path", savepath_xlsx="pathxlsx"):
        """
        Segment cancer cells in the low-resolution image and save the resulting segmentation and segmentation statistics.

        :param savepath: path to save segmentation outcome
        :param background_substracted_path: path to save background substracted image (optional)
        :param savepath_xlsx:  path to save segmentation statistics
        """

        # downsample 3D volume so that it can be handled by GPU.
        im_rescaled = ndimage.zoom(self.image_tosegment,
                                   [1., 1. / self.lateral_axialratio, 1. / self.lateral_axialratio], order=1,
                                   mode='reflect')


        input_gpu = cle.push(im_rescaled)

        # pre-processing: top hat box filter
        background_subtracted = cle.top_hat_box(input_gpu, radius_x=6, radius_y=6, radius_z=6)

        if background_substracted_path != "path":
            imwrite(background_substracted_path, background_subtracted)

        # greater constant
        image_constant_applied = cle.greater_constant(background_subtracted, None, 300.0)

        # segmentation: apply voronoi otsu labeling to binary image.
        image2_vol = cle.voronoi_otsu_labeling(image_constant_applied, None, 1.0, 2.0)

        # post-processing: exclude small labels
        image5_E = cle.exclude_small_labels(image2_vol, maximum_size=100.0)
        segmented_array = cle.pull(image5_E)

        #get segmentation statistics
        statistics = cle.statistics_of_labelled_pixels(input_gpu, segmented_array)
        table = pd.DataFrame(statistics)
        print("nb rows:" + str(table.shape[0]))
        if table.shape[0] < 256:
            imwrite(savepath, segmented_array.astype("uint8"))
        else:
            imwrite(savepath, segmented_array.astype("uint16"))

        if background_substracted_path != "pathxlsx":
            table.to_excel(savepath_xlsx)

    def iterate_throughfolder(self, parentfolder, resultsfolder, channellist):
        """
        Iterate through a folder with rawdata that should be segmented, generate filenames and calls the segmentation folders.

        :param parentfolder: folder through which to iterate
        :param resultsfolder: folder where to save the outcome
        :param channellist: iterate through channels
        """

        #obtain a list of all timepoint folders in the parentfolder
        dir_list = os.listdir(parentfolder)
        print(dir_list)
        timepointlist = []

        for path in dir_list:
            if path.startswith('t'):
                timepointlist.append(path)
        timepointlist.sort()

        print(timepointlist)

        for i_time in timepointlist:
            timepoint = i_time

            #iterate through the channels.
            for i_channel in range(len(channellist)):

                #define filenames
                channel = channellist[i_channel]
                whichfile = channel + '.tif'
                whichfile_sg = channel + 'sg.tif'
                csvfilename = timepoint + ".xlsx"

                # construct filepath
                imagefilepath = os.path.join(parentfolder, timepoint, whichfile)
                print(imagefilepath)

                resultfilefolder = os.path.join(resultsfolder, channel, timepoint)
                resultfilepath_sg = os.path.join(resultfilefolder, whichfile_sg)
                resultfilepath_bg = os.path.join(resultfilefolder, "background_test.tif")
                csvfolderpath = os.path.join(resultsfolder + "_xlsx", channel)
                csvfilefolderpath = os.path.join(csvfolderpath, csvfilename)

                # make folders
                try:
                    os.makedirs(resultfilefolder)
                except OSError as error:
                    pass
                try:
                    os.makedirs(csvfolderpath)
                except OSError as error:
                    pass

                # open image
                self.open_image(imagefilepath)

                # segment
                if channel == '1_CH488_000000':
                    self.segment_macrophage(resultfilepath_sg, savepath_xlsx=csvfilefolderpath, background_substracted_path=resultfilepath_bg)
                else:
                    self.segment_cancercells(resultfilepath_sg, savepath_xlsx=csvfilefolderpath)



if __name__ == '__main__':

    #init low res segmentation class
    segment_class = segment_macrophage_lowres_class()

    #parameters-----------------------------------
    parentfolder = "/archive/bioinformatics/Danuser_lab/Fiolka/Manuscripts/2023-multiscale/rawdata/12791724/Exemplary_Segmentation/Low_resolution/fish1"
    resultsfolder = parentfolder + "_segmented"
    channellist = ['1_CH488_000000', '1_CH552_000000']

    #perform actions
    segment_class.iterate_throughfolder(parentfolder, resultsfolder, channellist)


