"""
Sript to analyze the Shannon entropy over an entire image series.
"""

import numpy as np
from scipy.fftpack import dctn
import skimage.measure as skmeasure
import os
from tifffile import imread, imwrite
import matplotlib.pyplot as plt
import pandas as pd


def fast_normalized_dct_shannon_entropy(input_image, frequencycutoff):
    """
    Calculates the normalized DCT Shannon entropy of an image.
    Function from:  https://github.com/TheDeanLab/navigate/tree/develop/src/navigate/model/analysis

    :param input_image : np.ndarray
    :param frequencycutoff: determines which percentage of all frequencies are contributing to the entropy
        (rationale: you don't want to include noise/high frequencies in the image metric)
    :return: entropy value
    """

    dct_array = dctn(input_image, type=2)
    abs_array = np.abs(dct_array / np.linalg.norm(dct_array))
    yh = int(input_image.shape[1] // frequencycutoff)
    xh = int(input_image.shape[0] // frequencycutoff)
    entropy = (
        -2 * np.nansum(abs_array[:xh, :yh] * np.log2(abs_array[:xh, :yh])) / (yh * xh)
    )

    return np.atleast_1d(entropy)

def load_image(filename):
    """
    Load an image from disk.

    :param filename: filepath to image
    :return: np.array (image stack)
    """
    input_image = imread(filename)
    return input_image

if __name__ == '__main__':

    parentfolder = "/archive/bioinformatics/Danuser_lab/Fiolka/LabMembers/Stephan/multiscale_data/revision_experiments/ShannonEntropyExample/timeseries"
    result_xlsxfile = "/archive/bioinformatics/Danuser_lab/Fiolka/LabMembers/Stephan/multiscale_data/revision_experiments/ShannonEntropyExample/ShannonEntropyValues.xlsx"

    #get all timepoints from folder
    dir_list = os.listdir(parentfolder)
    timepointlist = []
    for path in dir_list:
        if path.startswith('t'):
            timepointlist.append(path)
    timepointlist.sort()

    # iterate over folder
    DCT_array = np.zeros(len(timepointlist))
    for i in range(0,len(timepointlist)):
        image = load_image(os.path.join(parentfolder, timepointlist[i]))
        DCT_array[i] = fast_normalized_dct_shannon_entropy(image, 3)[0]

    #plot result
    plt.plot(range(0,len(timepointlist)), DCT_array)
    plt.show()

    ## save to xlsx file
    df = pd.DataFrame(DCT_array)
    df.to_excel(result_xlsxfile, index=False)
    print("done")

