
import numpy as np
import napari
import os
import cupy as cp
import skimage.transform
from tifffile import imread, imwrite

class image_visualizer_stitched():
    """
       This class generates visualizations of low-resolution segmentation results.
       """

    def __init__(self):
        """
        Initialize data folders and start Napari
        """

        #initialize data folders
        rawdatafolder_parent = "folderpath"
        self.rawdatafolder = "rawdatafolder"
        self.segmentationfolder = "segmenteddatafolder"
        self.visualizedfolder = "outputfolder"

        #start napari viewer
        self.viewer = napari.Viewer()

    def load_visualize_images(self, vis_param):
        """
        Load images from folder and render them according Visualization parameters specified.

        :param vis_param: Python dictionary of visulization paramters, e.g. vis_param['camera_angle1']
        """

        # get all timepoints from folder
        dir_list = os.listdir(self.segmentationfolder)
        timepointlist = []
        for path in dir_list:
            if path.startswith('t'):
                timepointlist.append(path)
        timepointlist.sort()

        # if you establish parameters, only open first timepoint
        if vis_param['establish_param'] == 1:
            timepointlist = ["t00000"]

        for i_time in timepointlist:

            # generate filepaths and folders
            segmentedimagepath = os.path.join(self.segmentationfolder, i_time, "1_CH488_000000sg.tif")
            segmentedimagepath_red = os.path.join(self.segmentationfolder, i_time, "1_CH488_000000sg_red.tif")
            segmentedimagepath_blue = os.path.join(self.segmentationfolder, i_time, "1_CH488_000000sg_blue.tif")
            segmentedimagepath_green = os.path.join(self.segmentationfolder, i_time, "1_CH488_000000sg_green.tif")

            rawimagepath = os.path.join(self.rawdatafolder, i_time, "1_CH488_000000.tif")
            rawimagepath_vessels = os.path.join(self.rawdatafolder, i_time, "1_CH594_000000.tif")

            visualization_folder1 = os.path.join(self.visualizedfolder,  "angle_1a")
            visualization_folder2 = os.path.join(self.visualizedfolder, "angle_2a")

            try:
                os.makedirs(visualization_folder1)
            except OSError as error:
                pass
            try:
                os.makedirs(visualization_folder2)
            except OSError as error:
                pass

            visualized_file = os.path.join(visualization_folder1, i_time + ".tif")
            visualized_file2 = os.path.join(visualization_folder2, i_time + ".tif")

            # open images
            input_image_raw = imread(rawimagepath)
            input_image_vessel_raw = imread(rawimagepath_vessels)
            label_image = imread(segmentedimagepath)
            label_image_red = imread(segmentedimagepath_red)
            label_image_blue = imread(segmentedimagepath_blue)
            label_image_green = imread(segmentedimagepath_green)

            print(input_image_raw.shape)

            #downsample huge low-resolution raw images to same size as label images (which are isotropic in voxel size)
            input_image = skimage.transform.resize(input_image_raw, label_image.shape, order=0)
            input_image_vessels = skimage.transform.resize(input_image_vessel_raw, label_image.shape, order=0)


            print(input_image.shape)
            print(label_image.shape)

            # add images as layers
            image_layer = self.viewer.add_image(input_image, gamma=vis_param['raw_gamma'], contrast_limits=vis_param['raw_contrast_limits'])
            image_layer_vessels = self.viewer.add_image(input_image_vessels, gamma=vis_param['raw_gamma_vessel'], contrast_limits=vis_param['raw_contrast_limits_vessels'], blending=vis_param['blending1'])
            layer_image_rescaled = self.viewer.add_labels(label_image, opacity=vis_param['label_opacity'], blending=vis_param['blending1'])
            layer_image_red = self.viewer.add_image(label_image_red, opacity=vis_param['label_opacity'], blending=vis_param['blending2'], colormap='red')
            layer_image_blue = self.viewer.add_image(label_image_blue, opacity=vis_param['label_opacity'], blending=vis_param['blending2'],colormap='blue')
            layer_image_green = self.viewer.add_image(label_image_green, opacity=vis_param['label_opacity'], blending=vis_param['blending2'], colormap='green')
            layer_image_green.visible='true' #interesting hack to make it display colors

            # set rendering to 3D and set camera zoom parameters
            self.viewer.dims.ndisplay = vis_param['rendering_dimension']
            self.viewer.camera.zoom = vis_param['camera_zoom']

            # save a first camera position
            self.viewer.camera.angles = vis_param['camera_angle1']
            imagereturn = self.viewer.screenshot(canvas_only=True, scale=vis_param['scale_to_save'])
            imwrite(visualized_file, imagereturn)

            # if you want to save a second camera position
            # get angle from napari by entering: viewer.camera.angles in console
            self.viewer.camera.angles = vis_param['camera_angle2']
            imagereturn2 = self.viewer.screenshot(canvas_only=True,scale=vis_param['scale_to_save'])
            imwrite(visualized_file2, imagereturn2)

            # if you establish the parameters, run napari, otherwise delete the layers for next timepoint
            if vis_param['establish_param']==1:

                napari.run()
            else:
                self.viewer.layers.remove('input_image')
                self.viewer.layers.remove('label_image')
                self.viewer.layers.remove('input_image_vessels')
                self.viewer.layers.remove('label_image_red')
                self.viewer.layers.remove('label_image_green')
                self.viewer.layers.remove('label_image_blue')


if __name__ == '__main__':
    #vis_param = visualization_param
    visualization_param = dict(
        camera_angle1 = (169, -18, 72),
        camera_angle2 = (18, -53, -120),
        camera_zoom=0.7,
        raw_contrast_limits=(300, 1400),
        raw_contrast_limits_vessels=(600, 15027),
        raw_gamma=0.9,
        raw_gamma_vessel=0.5,
        label_opacity=0.51,
        rendering_dimension=3,
        blending1='translucent',
        blending2='additive',
        establish_param=0,
        scale_to_save=5
    )

    imagevisu = image_visualizer_stitched()
    rawdatafolder_parent = "/archive/bioinformatics/Danuser_lab/Fiolka/Manuscripts/2023-multiscale/rawdata/12791724/Exemplary_VisualizationDataset"
    imagevisu.rawdatafolder = os.path.join(rawdatafolder_parent, "low_resolution_rawdata")
    # segmented data
    imagevisu.segmentationfolder = os.path.join(rawdatafolder_parent, "low_resolutionsegmentation_labelimages")
    imagevisu.visualizedfolder = imagevisu.rawdatafolder + "_visualized"
    imagevisu.load_visualize_images(visualization_param)

