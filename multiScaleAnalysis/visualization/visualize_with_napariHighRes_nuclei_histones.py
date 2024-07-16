import numpy as np
import napari
import os

import skimage.transform
from tifffile import imread, imwrite

class image_visualizer2():
    """
       This class generates visualizations of highres segmentation results.
       """

    def __init__(self):
        """
        Initialize data folders and start Napari
        """

        self.rawdatafolder = "rawdatafolder"
        self.segmentationfolder = "segmenteddatafolder"
        self.visualizedfolder = "outputfolder"
        self.region = "high_stack_001"
        self.establish_param = 0

        self.viewer = napari.Viewer()


    def load_images(self, vis_param):
        """"
        Load images from folder and render them according visualization parameters specified.

        :param vis_param: Python dictionary of visulization paramters, e.g. vis_param['camera_angle1']
        """
        #get all timepoints from folder
        image_list = os.listdir(self.rawdatafolder)

        image_list.sort()

        if self.establish_param==1:
            image_list =[image_list[0]]

        for i_time in image_list:
            #generate filepaths and folders
            rawimagepath_histones = os.path.join(self.rawdatafolder, i_time)
            print(rawimagepath_histones)
            visualization_folder1 = os.path.join(self.visualizedfolder, self.region, "angle_1a")
            visualization_folder2 = os.path.join(self.visualizedfolder, self.region, "angle_2a")
            visualization_folder3 = os.path.join(self.visualizedfolder, self.region, "angle_2a_frame")

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
            visualized_file = os.path.join(visualization_folder1,  i_time)
            visualized_file2 = os.path.join(visualization_folder2, i_time )
            visualized_file3 = os.path.join(visualization_folder3, i_time )

            #open images
            input_image = imread(rawimagepath_histones)


            #add images as layers
            image_layer = self.viewer.add_image(input_image, gamma=vis_param['raw_gamma'], contrast_limits=vis_param['raw_contrast_limits'], colormap=vis_param['raw_colormap'])

            #set rendering to 3D and set camera zoom parameters
            self.viewer.dims.ndisplay = vis_param['rendering_dimension']
            self.viewer.camera.zoom = vis_param['camera_zoom']

            #rescale 3D data to be correct dimensions
            self.viewer.layers['input_image'].scale = vis_param['raw_rescale_factor']

            #interpolation to cubic
            self.viewer.layers['input_image'].interpolation3d ='cubic'

            #save a first camera position
            self.viewer.camera.angles = vis_param['camera_angle1']
            imagereturn = self.viewer.screenshot(canvas_only=True, scale=vis_param['scale_to_save'])
            imwrite(visualized_file, imagereturn)

            #save without vasculature
            #get angle from napari by entering: viewer.camera.angles in console
            self.viewer.camera.angles = vis_param['camera_angle2']
            #self.viewer.layers.remove('cancer_image')

            imagereturn2 = self.viewer.screenshot(canvas_only=True, scale=vis_param['scale_to_save'])
            imwrite(visualized_file2, imagereturn2)

            self.viewer.layers['input_image'].bounding_box.visible = True
            imagereturn3 = self.viewer.screenshot(canvas_only=True, scale=vis_param['scale_to_save'])
            imwrite(visualized_file3, imagereturn3)

            #if you establish the parameters, run napari, otherwise delete the layers for next timepoint
            if self.establish_param==1:
                napari.run()
            else:
                self.viewer.layers.remove('input_image')
                #self.viewer.layers.remove('cancer_image')




if __name__ == '__main__':

    visualization_param = dict(
        camera_angle1=(25.71195010907721, -21.600485468575528, 137.18437963747954),
        camera_angle2=(-154.05133249286894, 20.38038635676573, 47.39396029366354),
        camera_zoom=0.295,
        #raw_contrast_limits=(126,482),
        raw_contrast_limits=(50, 1150),
        raw_contrast_limits_cancer=(102, 1529),
        raw_gamma=0.67,
        raw_gamma_cancer=0.59,
        raw_colormap ='gray_r',
        cancer_colormap='gray',
        opacity_cancer=0.58,
        opacity_label=1,
        rendering_dimension=3,
        label_blending='additive',
        # raw_rescale_factor =[9.210526, 1, 1],
        # label_rescale_factor = [9.210526, 1, 1],
        raw_rescale_factor =[2.5, 1, 1],
        label_rescale_factor =[2.5, 1, 1],
        #raw_rescale_factor=[1, 1, 1],
        #label_rescale_factor=[1, 1, 1],
        establish_param=0,
        set_label_colormap='default',
        scale_to_save=5,
        display_rawcancersignal=0,
        imagename_raw="1_CH488_000000.tif"
    )
    imagevisu = image_visualizer2()

    imagevisu.rawdatafolder = "/archive/bioinformatics/Danuser_lab/Fiolka/Manuscripts/2023-multiscale/rawdata/nuclei_movie/Experiment005_cropped/high_resolution"
    experimentfolder_result = imagevisu.rawdatafolder + "_highres_visualized"
    imagevisu.segmentationfolder = os.path.join(experimentfolder_result, 'high_stack_001')
    imagevisu.visualizedfolder = os.path.join(experimentfolder_result, 'visualized_3')
    imagevisu.region = 'high_stack_001'
    imagevisu.establish_param = 0
    imagevisu.load_images(visualization_param)






