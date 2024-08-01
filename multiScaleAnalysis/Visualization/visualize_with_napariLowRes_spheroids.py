import numpy as np
import napari
import os

import skimage.transform
from tifffile import imread, imwrite

class image_visualizer():
    """
       This class generates visualizations of low-resolution rawdata of spheroids.
       """

    def __init__(self):
        """
        Initialize data folders and start Napari
        """

        # initialize data folders
        rawdatafolder_parent = "folderpath"
        self.rawdatafolder = "rawdatafolder"
        self.segmentationfolder = "segmenteddatafolder"
        self.visualizedfolder = "outputfolder"

        # start napari viewer
        self.viewer = napari.Viewer()


    def load_images(self, vis_param):
        """
        Load images from folder and render them according Visualization parameters specified.

        :param vis_param: Python dictionary of visulization paramters, e.g. vis_param['camera_angle1']
        """
        #get all timepoints from folder
        dir_list = os.listdir(self.rawdatafolder)
        timepointlist = []
        for path in dir_list:
            if path.startswith('t'):
                timepointlist.append(path)
        timepointlist.sort()
        print(timepointlist)
        #if you establish parameters, only open first timepoint
        if self.establish_param==1:
            timepointlist = ["t00000"]
            i_time="t00000"

        for i_time in timepointlist:
            print(i_time)
            #generate filepaths and folders
            rawimagepath_spheroid_magenta = os.path.join(self.rawdatafolder, i_time, vis_param['imagename_magenta'])
            rawimagepath_spheroid_cyan  = os.path.join(self.rawdatafolder, i_time, vis_param['imagename_cyan'])

            visualization_folder1 = os.path.join(self.visualizedfolder,  "angle_1a")
            visualization_folder2 = os.path.join(self.visualizedfolder,  "angle_2a")
            visualization_folder3 = os.path.join(self.visualizedfolder, "angle_2a_frame")

            try:
                os.makedirs(visualization_folder1)
            except OSError as error:
                pass
            try:
                os.makedirs(visualization_folder2)
            except OSError as error:
                pass
            try:
                os.makedirs(visualization_folder3)
            except OSError as error:
                pass

            visualized_file = os.path.join(visualization_folder1,  i_time + ".tif")
            visualized_file2 = os.path.join(visualization_folder2, i_time + ".tif")
            visualized_file3 = os.path.join(visualization_folder3, i_time + ".tif")

            #open images
            image_magentabig = imread(rawimagepath_spheroid_magenta)
            image_cyanbig= imread(rawimagepath_spheroid_cyan)
            print(image_magentabig.shape)

            # downsample huge low-resolution raw images to same size as label images (which are isotropic in voxel size)
            image_magenta = skimage.transform.resize(image_magentabig, output_shape=(200, 666, 1000), order=0)
            image_cyan = skimage.transform.resize(image_cyanbig, output_shape=(200, 666, 1000), order=0)

            #add images as layers
            image_layer = self.viewer.add_image(image_magenta, gamma=vis_param['raw_gamma_magenta'], contrast_limits=vis_param['raw_contrast_limits_magenta'], colormap=vis_param['magenta_colormap'])
            cancer_layer = self.viewer.add_image(image_cyan, gamma=vis_param['raw_gamma_cyan'], opacity=vis_param['opacity_cyan'], contrast_limits=vis_param['raw_contrast_limits_cyan'], colormap=vis_param['cyan_colormap'], blending='additive')

            #set rendering to 3D and set camera zoom parameters
            self.viewer.dims.ndisplay = vis_param['rendering_dimension']
            self.viewer.camera.zoom = vis_param['camera_zoom']

            #rescale 3D data to be correct dimensions
            self.viewer.layers['image_magenta'].scale = vis_param['raw_rescale_factor']
            self.viewer.layers['image_cyan'].scale = vis_param['raw_rescale_factor']

            #interpolation to cubic
            self.viewer.layers['image_magenta'].interpolation3d ='cubic'
            self.viewer.layers['image_cyan'].interpolation3d ='cubic'

            #save a first camera position
            #get angle from napari by entering: viewer.camera.angles in console
            self.viewer.layers['image_cyan'].bounding_box.visible=False

            self.viewer.camera.angles = vis_param['camera_angle1']
            imagereturn = self.viewer.screenshot(canvas_only=True, scale=vis_param['scale_to_save'])
            imwrite(visualized_file, imagereturn)

            #save a second camera position
            self.viewer.camera.angles = vis_param['camera_angle2']
            imagereturn2 = self.viewer.screenshot(canvas_only=True, scale=vis_param['scale_to_save'])
            imwrite(visualized_file2, imagereturn2)

            self.viewer.layers['image_cyan'].bounding_box.visible=True
            imagereturn3 = self.viewer.screenshot(canvas_only=True, scale=vis_param['scale_to_save'])
            imwrite(visualized_file3, imagereturn3)

            #if you establish the parameters, run napari, otherwise delete the layers for next timepoint
            if self.establish_param==1:
                napari.run()
            else:
                self.viewer.layers.remove('image_magenta')
                self.viewer.layers.remove('image_cyan')




if __name__ == '__main__':

    visualization_param = dict(
        camera_angle1=(-90.12192998901911, -11.908473792258878, 59.457226017303086),
        camera_angle2=(7.6471045194606635, -20.182789486876842, 72.3066107960275),
        camera_zoom=0.42,
        raw_contrast_limits_magenta=(160, 2742),
        raw_contrast_limits_cyan=(335, 2944),
        raw_gamma_magenta=0.78,
        raw_gamma_cyan=0.76,
        magenta_colormap ='magenta',
        cyan_colormap='cyan',
        opacity_cyan=0.64,
        rendering_dimension=3,
        raw_rescale_factor =[3.58, 1, 1],
        establish_param=0,
        scale_to_save=5,
        imagename_cyan="1_CH488_000000.tif",
        imagename_magenta="1_CH594_000000.tif"

    )
    imagevisu = image_visualizer()

    imagevisu.rawdatafolder = "/archive/bioinformatics/Danuser_lab/Fiolka/Manuscripts/2023-multiscale/rawdata/Spheroid/Low_resolution/"
    experimentfolder_result = imagevisu.rawdatafolder + "_lowres_visualized_rotated"
    imagevisu.visualizedfolder = os.path.join(experimentfolder_result, 'visualized_frame')
    imagevisu.establish_param = 0
    imagevisu.load_images(visualization_param)

