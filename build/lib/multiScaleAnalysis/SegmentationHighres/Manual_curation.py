import copy

import numpy as np
import os
from tifffile import imread, imwrite
import skimage.color as skcolor
import seaborn as sns
from skimage.segmentation import relabel_sequential

class manual_curate_segmentation():
    """
    This class provides functions to manually curate images
    """

    def remove_label(self, stack, label):
        """
        Removes a specific label from a 3D image stack.

        :param stack: numpy array
        :param label: label
        :return: processed numpy array
        """
        currentlabel_indices = np.where(stack == label)
        stack[currentlabel_indices] = 0
        return stack

    def merge_label(self, stack, label1, label2):
        """
        Merge labels (replaces label2 with label1)

        :param stack: numpy array to process
        :param label1: integer label
        :param label2: integer label
        :return: processed numpy array
        """
        currentlabel_indices = np.where(stack == label2)
        stack[currentlabel_indices] = label1
        return stack

    def takeLabel_fromanotherstack(self, stack, anotherstack, label):
        """
        Take a label from another stack (anotherstack) and insert it into the current stack (stack).

        :param stack: numpy array to process
        :param anotherstack: numpy array to take label from
        :param label: label to take
        :return: processed numpy array
        """

        anotherstack_indices = np.where(anotherstack == label)
        maximumlabel = np.max(stack)
        newlabel = anotherstack[anotherstack_indices] + maximumlabel + 1
        stack[anotherstack_indices] = anotherstack[anotherstack_indices] + maximumlabel + 1
        return stack, newlabel[0]

    def takeLabel_fromanotherstack_range(self, stack, anotherstack_orig, label, xrange=[], yrange=[], zrange=[]):
        """
        Take a label from another stack (anotherstack) and insert it into the current stack (stack).

        :param stack: numpy array to process
        :param anotherstack: numpy array to take label from
        :param label: label to take
        :param xrange: narrow down where to take the label from (range in x/shape[1])
        :param yrange: narrow down where to take the label from (range in y/shape[2])
        :param zrange: narrow down where to take the label from (range in z/shape[0])
        :return: processed numpy array
        """
        anotherstack = copy.deepcopy(anotherstack_orig)
        if not zrange:
            zrange = [0, anotherstack.shape[0]]
        if not xrange:
            xrange = [0, anotherstack.shape[1]]
        if not yrange:
            yrange = [0, anotherstack.shape[2]]

        #make boundingbox and bound image
        binarybox = np.zeros(anotherstack.shape)
        binarybox[zrange[0]:zrange[1], xrange[0]:xrange[1], yrange[0]:yrange[1]]=1

        selectedimage = binarybox * anotherstack

        #select only specific labels
        anotherstack_indices = np.where(selectedimage == label)

        maximumlabel = np.max(stack)

        newlabel = anotherstack[anotherstack_indices] + maximumlabel + 1
        stack[anotherstack_indices] = anotherstack_orig[anotherstack_indices] + maximumlabel + 1

        return stack, newlabel[0]

    def replace_one_label(self, stack, anotherstack, labeltoreplace):
        """
        Replace all positions in a stack with a defined label (labeltoreplace) with unique labels of anotherstack at these positions.

        :param stack: np.array to replace a label
        :param anotherstack: take the label id from this stack for all position with labeltoreplace in stack
        :param labeltoreplace: label to replace
        :return: modified stack
        """

        # make binary 0 or 1
        im_binary = anotherstack > 0.5
        currentlabel_indices = np.where(stack == labeltoreplace)
        maximumlabel = np.max(stack)

        stack[currentlabel_indices] = im_binary[currentlabel_indices] * (anotherstack[currentlabel_indices] + maximumlabel + 1)
        return stack

    def give_label_new_identiyinarea(self, stack, label, xrange=[], yrange=[], zrange=[]):
        """
        Find a label in (xrange, yrange, zrange) and give it a new unique label

        :param stack: numpy array to process
        :param label: label to modify
        :param xrange: narrow down where to modify the label (range in x/shape[1])
        :param yrange: narrow down where to modify the label (range in y/shape[2])
        :param zrange: narrow down where to modify the label (range in z/shape[0])
        :return: modified np.array, new unique label
        """
        anotherstack = copy.deepcopy(stack)
        if not zrange:
            zrange = [0, anotherstack.shape[0]]
        if not xrange:
            xrange = [0, anotherstack.shape[1]]
        if not yrange:
            yrange = [0, anotherstack.shape[2]]

        # make boundingbox and bound image
        binarybox = np.zeros(anotherstack.shape)
        binarybox[zrange[0]:zrange[1], xrange[0]:xrange[1], yrange[0]:yrange[1]] = 1

        selectedimage = binarybox * anotherstack

        # select only specific labels
        anotherstack_indices = np.where(selectedimage == label)

        maximumlabel = np.max(stack)

        newlabel = anotherstack[anotherstack_indices] + maximumlabel + 1
        stack[anotherstack_indices] = stack[anotherstack_indices] + maximumlabel + 1

        return stack, newlabel[0]

    def saveimage(self, new_image, path_save, path_save_RGB):
        """
        Save the image to disk

        :param new_image: image to save
        :param path_save: path to save label image
        :param path_save_RGB: path to save label image with RGB color labels.
        """
        # relabel image so that labels go from 1 to x
        relab, fw2, inv2 = relabel_sequential(new_image)
        # save new curated
        imwrite(path_save, relab)
        color_image = np.uint8(255 * skcolor.label2rgb(relab.copy(),
                                                       colors=sns.color_palette('hls', n_colors=16),
                                                       bg_label=0))
        imwrite(path_save_RGB, np.uint8(color_image))





if __name__ == "__main__":
    # =============================================================================
    # initializations
    # =============================================================================
    region = "high_stack_002"
    timepoint = "t00049"
    parentfolder = "/archive/bioinformatics/Danuser_lab/Fiolka/LabMembers/Stephan/multiscale_data/xenograft_experiments/U2OS_WT/20220729_Daetwyler_U2OS"
    data_segmentation = os.path.join(parentfolder, "Experiment0001_highresSeg_connectedComp_multiOtsu", "processed_segmentation_merged130", region, timepoint, "labels_xy-merged.tif")
    data_before_processing = os.path.join(parentfolder, "Experiment0001_highresSeg_connectedComp_multiOtsu", "result_segmentation", region, timepoint, "labels_xy-connectedcomponents.tif")
    data_cellpose =  os.path.join(parentfolder, "Experiment0001_highresSeg_run_again", "result_segmentation", region, timepoint, "labels_xy-integrated_gradients-correct_noexpand.tif")
    data_segmentation = os.path.join(parentfolder, "Experiment0001_highres_manuallyCompiled",  region, timepoint, "labels_xy-merged.tif")

    path_save_folder = os.path.join(parentfolder, "Experiment0001_highres_manuallyCompiled2", region, timepoint)
    path_save = os.path.join(path_save_folder, "labels_xy-merged.tif")
    path_save_RGB = os.path.join(path_save_folder, "labels_xy-merged_componentsRGB.tif")
    try:
        os.makedirs(path_save_folder)
    except OSError as error:
        pass


    """parameters"""
    curate_it = manual_curate_segmentation()

    new_image = imread(data_segmentation)
    multiOtsu_segmentation = imread(data_before_processing)
    cellpose_segmentation = imread(data_cellpose)


    # example t00027
    # new_image = curate_it.merge_label(new_image, 17, 20)
    # new_image = curate_it.merge_label(new_image, 14, 26)
    # new_image = curate_it.merge_label(new_image, 21, 22)
    # new_image, newlabel = curate_it.takeLabel_fromanotherstack(new_image, cellpose_segmentation, 100)
    # new_image = curate_it.merge_label(new_image, 24, newlabel)
    # new_image = curate_it.replace_one_label(new_image, cellpose_segmentation, 23)

    # save image
    curate_it.saveimage(new_image, path_save, path_save_RGB)


