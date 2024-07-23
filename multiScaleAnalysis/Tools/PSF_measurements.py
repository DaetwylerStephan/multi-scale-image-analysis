"""
Script to analyze the PSF values over an entire image.
"""

import skimage.filters as skfilters
from tifffile import imread, imwrite
import skimage.measure as skmeasure
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

def load_image(filename):
    """
    Load an image from disk.

    :param filename: filepath to image
    :return: np.array (image stack)
    """
    print(f'load: {filename}')
    input_image = imread(filename)
    return input_image

def binarize_label_image(image, threshold):
    """
    Binarize and label individual beads in image.

    :param image: np.array /3D image to analyze
    :param threshold: selected threshold to identify beads
    :return: np.array with labelled beads
    """
    im_binary = image > (threshold) # +0.1;
    connected_components_labels = skmeasure.label(im_binary > 0)
    return connected_components_labels

def get_centroidpositions(props):
    """
    Return the centroids as an array from region props.

    :param props: Region properties construct
    :return: np.array(n beads, 3) with centroid positions
    """
    centroidarray = np.zeros(shape=(np.size(props), 3)).astype("int")
    for i in range(0,np.size(props)):
        centroidarray[i] = np.round(props[i].centroid).astype("int")
    return centroidarray

def filter_centroidpositions(centroidlist, areaarray, im_shape, axial_dist=5, lateral_dist=10, areacutoff=300):
    """
    Filter the centroid positions to remove beads at the edge and beads that are too big (not point sources)
    or too small.

    :param centroidlist: list of centroid positions
    :param areaarray:
    :param im_shape:
    :param axial_dist:
    :param lateral_dist:
    :param areacutoff: largest area/volume acceptable for a bead
    """

    centroidarray_filtered_v1 = np.zeros(shape=centroidlist.shape).astype("int")
    iternumber = 0
    for i in range(0, len(centroidlist)):
        if centroidlist[i][0]-axial_dist<0 or centroidlist[i][0]+axial_dist> im_shape[0]:
            continue
        if centroidlist[i][1] - lateral_dist < 0 or centroidlist[i][1]+lateral_dist > im_shape[1]:
            continue
        if centroidlist[i][2] - lateral_dist < 0 or centroidlist[i][2]+lateral_dist > im_shape[2]:
            continue
        if areaarray[i]>areacutoff or areaarray[i]<3:
            continue

        centroidarray_filtered_v1[iternumber]= centroidlist[i]
        iternumber = iternumber + 1

    centroidarray_filtered = np.zeros(shape=(iternumber,3)).astype("int")
    centroidarray_filtered = centroidarray_filtered_v1[0:iternumber,:]
    return centroidarray_filtered

def Gauss(x, a, b, c, d):
    """

    Definition of a Gaussian function for fitting:
    # y = a + (b-a) * np.exp(-(x-c)**2/(2 * d ** 2))

    :param x: x variable
    :param a: a parameter
    :param b: b parameter
    :param c: c parameter
    :param d: d parameter

    """
    # Define the Gaussian function
    y = a + (b-a) * np.exp(-(x-c)**2/(2 * d ** 2))
    return y

def determinePSFvalues(croppedimage, lateralstepsize=0.117, axialstepsize = 0.2):
    """
    Determine the point spread function (PSF) value of a single bead in a cropped image.

    :param croppedimage: image containing a single bead.
    :param lateralstepsize: Physical dimension of voxel in lateral direction.
    :param axialstepsize: Physical dimension of voxel in axial direction.
    :return: PSF value array: [lateralX_FWHM, lateralY_FWHM, axial_FWHM], returns nan if no
             Gaussian fit to the function could be found.
    """
    # find max index
    ind = np.unravel_index(np.argmax(croppedimage, axis=None), croppedimage.shape)

    #axialPSF
    lineZ = croppedimage[:,ind[1],ind[2]]
    xdata = axialstepsize * np.array(range(0,len(lineZ)))

    try:
        parametersZ, covariance = curve_fit(Gauss, xdata, lineZ)
        axial_FWHM = np.abs(parametersZ[3])*2.355
    except:
        axial_FWHM = float("nan")

    #lateralPSF
    lineY = croppedimage[ind[0],:,ind[2]]
    xdata = lateralstepsize * np.array(range(0,len(lineY)))
    try:
        parametersY, covariance = curve_fit(Gauss, xdata, lineY)
        lateralY_FWHM = np.abs(parametersY[3])*2.355
    except:
        lateralY_FWHM = float("nan")

    # lateralPSF
    lineX = croppedimage[ind[0], ind[1], :]
    xdata = lateralstepsize * np.array(range(0, len(lineX)))
    try:
        parametersX, covariance = curve_fit(Gauss, xdata, lineX)
        lateralX_FWHM = np.abs(parametersX[3]) * 2.355
    except:
        lateralX_FWHM = float("nan")

    PSF_array = [lateralX_FWHM, lateralY_FWHM, axial_FWHM]
    return PSF_array


def get_psfvalues(image, centroidlist_filtered, axial_dist=5, lateral_dist=10, lateralstepsize=0.117, axialstepsize=0.2):
    """
    Iterate over all beads in an image and generate an image crop for each bead. Calls the determinePSFvalues function
    to calculate the point spread function (PSF) value of the bead in the image crop, and enter the obtained PSF value
    into a list of PSF values.

    :param image: np.array/image with beads
    :param centroidlist_filtered: List of centroid positions.
    :param axial_dist: An image crop is generated with extend of centroid_z +/- axial_dist to calculate the PSF.
    :param lateral_dist: An image crop is generated with extend of centroid_x +/- lateral_dist and centroid_y +/- lateral_dist to calculate the PSF.
    :param lateralstepsize: Physical dimension of voxel in lateral direction.
    :param axialstepsize: Physical dimension of voxel in axial direction.
    :return: An array of PSF values
    """

    psf_values_array = np.zeros(shape=(len(centroidlist_filtered), 6)).astype("float")


    for i in range(0,len(centroidlist_filtered)):
        # get roi of bead
        psf_values_array[i][0]=centroidlist_filtered[i][0]
        psf_values_array[i][1]=centroidlist_filtered[i][1]
        psf_values_array[i][2]=centroidlist_filtered[i][2]

        #generate image crop
        testimage = image[centroidlist_filtered[i][0] - axial_dist:centroidlist_filtered[i][0] + axial_dist,
                    centroidlist_filtered[i][1] - lateral_dist:centroidlist_filtered[i][1] + lateral_dist,
                    centroidlist_filtered[i][2] - lateral_dist:centroidlist_filtered[i][2] + lateral_dist]

        psf_results = determinePSFvalues(testimage, lateralstepsize, axialstepsize)
        psf_values_array[i][3] = psf_results[0]
        psf_values_array[i][4] = psf_results[1]
        psf_values_array[i][5] = psf_results[2]

    return psf_values_array


def filter_psfvalues(psf_list, highestlateralvalue=1, highestaxialvalue = 2):
    """
    Filter the PSF values to remove clustered beads/aggregates etc.

    :param psf_list: list of psf values
    :param highestlateralvalue: highest expected lateral value from a single bead
    :param highestaxialvalue: highest expected axial value from a single bead
    :return: filtered list of psf values
    """
    psfvalues_filtered_v1 = np.zeros(shape=psf_list.shape)

    iternumber = 0
    for i in range(0, len(psfvalues_filtered_v1)):
        if psf_list[i][3] > highestlateralvalue or np.isnan(psf_list[i][3]):
            continue
        if psf_list[i][4] > highestlateralvalue or np.isnan(psf_list[i][4]):
            continue
        if psf_list[i][5] > highestaxialvalue or np.isnan(psf_list[i][5]):
            continue
        psfvalues_filtered_v1[iternumber]= psf_list[i]
        iternumber = iternumber + 1

    psfvalues_filtered = np.zeros(shape=(iternumber,3)).astype("int")
    psfvalues_filtered = psfvalues_filtered_v1[0:iternumber,:]
    return psfvalues_filtered



if __name__ == '__main__':

    # generate file paths
    parentfolder = "/archive/bioinformatics/Danuser_lab/Fiolka/Manuscripts/2023-multiscale/rawdata/12791724/Exemplary_PSFcharaterization/"

    imagefilepath = parentfolder + "1_CH488_000000.tif"  # rawimage name
    imagefilepath_labelled = parentfolder + "1_CH488_000000labelled.tif"  # save image with bead positions
    imagefilepath_plot = parentfolder + "psf_plot2.jpg"  # plot bead profiles along image/stack axis
    imagefilepath_Excelfile = parentfolder + "psf_values.xlsx"  # save bead positions and their values to Excel file
    imagefilepath_textfile = parentfolder + "psf_values.txt"  # save summary textfile

    # parameters
    threshold = 500
    lateral_dist = 10
    axial_dist = 6
    areacutoff = 300
    pixelvalue_lateral_um = 0.117
    pixelvalue_axial_um = 0.2
    cutoff_lateralPSFvalue = 1
    cutoff_axialPSFvalue = 2
    showbeadplot = True

    #load image
    image=load_image(imagefilepath)

    #find beads in image
    image_binary = binarize_label_image(image, threshold)
    props = skmeasure.regionprops(image_binary)

    #optional: save label image to see if all beads were identified
    imwrite(imagefilepath_labelled, image_binary.astype("uint16"))

    #get centroidlist and filter it to remove beads at the image borders
    centroidlist = get_centroidpositions(props)

    #get arealist
    areaarray = np.zeros(shape=(np.size(props))).astype("int")
    for i in range(0, np.size(props)):
        areaarray[i] = np.round(props[i].area).astype("int")

    #plot histogram of area values to make an informed guess about which bead areas are acceptable
    plt.hist(areaarray, density=True, bins=30, range=[0, 500])  # density=False would make counts
    plt.show()

    #get filtered list
    centroidlist_filtered = filter_centroidpositions(centroidlist, areaarray, image.shape, axial_dist=axial_dist,lateral_dist=lateral_dist, areacutoff=areacutoff)

    #get roi of bead to check if crop is good
    #imagefilepath_test = parentfolder + "test_bead.tif"
    # beadid = 3
    # croppedimage = image[centroidlist_filtered[beadid][0]-axial_dist:centroidlist_filtered[beadid][0]+axial_dist, centroidlist_filtered[beadid][1] - lateral_dist:centroidlist_filtered[beadid][1] + lateral_dist, centroidlist_filtered[beadid][2]-lateral_dist:centroidlist_filtered[beadid][2]+lateral_dist]
    # imwrite(imagefilepath_test, croppedimage.astype("uint16"))
    # psfvalue_array = determinePSFvalues(croppedimage)

    #obtain the psf values of all beads and filter the list
    psf_list = get_psfvalues(image, centroidlist_filtered, axial_dist, lateral_dist, lateralstepsize=pixelvalue_lateral_um, axialstepsize=pixelvalue_axial_um)
    psf_values_filtered = filter_psfvalues(psf_list, highestlateralvalue=cutoff_lateralPSFvalue, highestaxialvalue=cutoff_axialPSFvalue)

    #report values
    print(np.nanmedian(psf_values_filtered[:,3]))
    print(np.nanmedian(psf_values_filtered[:,4]))
    print(np.nanmedian(psf_values_filtered[:,5]))

    #plot values
    fig, axs = plt.subplots(2,3, figsize=(30, 15))
    axs[0, 0].scatter(psf_values_filtered[:,1], psf_values_filtered[:,3])
    axs[0, 0].set_xlabel('(position x)')
    axs[0, 0].set_ylabel('(lateral resolution x)')
    axs[0, 1].scatter(psf_values_filtered[:, 1], psf_values_filtered[:, 4])
    axs[0, 1].set_xlabel('(position x)')
    axs[0, 1].set_ylabel('(lateral resolution y)')
    axs[0, 2].scatter(psf_values_filtered[:,1], psf_values_filtered[:,5])
    axs[0, 2].set_xlabel('(position x)')
    axs[0, 2].set_ylabel('(axial resolution )')

    axs[1, 0].scatter(psf_values_filtered[:, 2], psf_values_filtered[:, 3])
    axs[1, 0].set_xlabel('(position y)')
    axs[1, 0].set_ylabel('(lateral resolution x)')
    axs[1, 1].scatter(psf_values_filtered[:, 2], psf_values_filtered[:, 4])
    axs[1, 1].set_xlabel('(position y)')
    axs[1, 1].set_ylabel('(lateral resolution y)')
    axs[1, 2].scatter(psf_values_filtered[:, 2], psf_values_filtered[:, 5])
    axs[1, 2].set_xlabel('(position y)')
    axs[1, 2].set_ylabel('(axial resolution )')
    fig.savefig(imagefilepath_plot)

    if showbeadplot ==True:
        plt.show()

    #save values as Excel file
    df = pd.DataFrame(psf_values_filtered)
    df.to_excel(imagefilepath_Excelfile, index=False)

    f = open(imagefilepath_textfile, "a")
    f.write("x: " + str(np.nanmedian(psf_values_filtered[:, 3])))
    f.write(" y: " + str(np.nanmedian(psf_values_filtered[:, 4])))
    f.write(" z: " + str(np.nanmedian(psf_values_filtered[:, 5])))
    f.write(" number of beads: " + str(len(psf_values_filtered)))
    f.close()