import numpy as np
import scipy.ndimage.filters as flt
import skimage.filters as flt
import warnings
import os


class ImagePreprocessing:
    """
    This class contains all functions to preprocess the light-sheet images for successful segmentation
    """
    def __init__(self):
        """
        Initialize the class.
        """
        pass

    def mkdir(self, folder):
        """
        Make folders if they do not exist.

        :param folder: path to folder
        :return: empty list
        """
        if not os.path.exists(folder):
            os.makedirs(folder)

        return []

    def normalize(self, x, pmin=2, pmax=99.8, axis=None, clip=False, eps=1e-20, dtype=np.float32):
        """
        Percentile-based image normalization.

        :param x: np.array to normalize
        :param pmin: lower percentile boundary
        :param pmax: upper percentile boundary
        :param axis: {int, tuple of int, None} (optional) Axis or axes along which the percentiles are computed. The
            default is to compute the percentile(s) along a flattened  version of the array.
        :param clip: clip values of normalized array to [0,1]
        :param eps: (optional) make sure that division is not zero with small value
        :param dtype: (optional) type used for calculations
        """
        mi = np.percentile(x, pmin, axis=axis, keepdims=True)
        ma = np.percentile(x, pmax, axis=axis, keepdims=True)
        return self.normalize_mi_ma(x, mi, ma, clip=clip, eps=eps, dtype=dtype)

    def normalize_mi_ma(self, x, mi, ma, clip=False, eps=1e-20, dtype=np.float32):
        """
        Minimal (mi) and maximal (ma) value based image normalization.

        :param x: np.array to normalize
        :param mi: lower boundary for normalization
        :param ma: upper boundary for normalization
        :param clip: clip values of normalized array to [0,1]
        :param eps: (optional) make sure that division is not zero with small value
        :param dtype: (optional) type used for calculations
        """

        if dtype is not None:
            x   = x.astype(dtype,copy=False)
            mi  = dtype(mi) if np.isscalar(mi) else mi.astype(dtype,copy=False)
            ma  = dtype(ma) if np.isscalar(ma) else ma.astype(dtype,copy=False)
            eps = dtype(eps)
        try:
            import numexpr
            x = numexpr.evaluate("(x - mi) / ( ma - mi + eps )")
        except ImportError:
            x =                   (x - mi) / ( ma - mi + eps )
        if clip:
            x = np.clip(x,0,1)
        return x

    def normalize99(self, Y, lower=0.01, upper=99.99):
        """
        Normalize image so 0.0 is 0.01st percentile and 1.0 is 99.99th percentile
        Upper and lower percentile ranges configurable.

        :param Y: ndarray, float. Component array of length N by L1 by L2 by ... by LN.
        :param upper: float. Upper percentile above which pixels are sent to 1.0
        :param lower: float. Lower percentile below which pixels are sent to 0.0
        :return: Normalized array with a minimum of 0 and maximum of 1
        """
        X = Y.copy()
        return np.interp(X, (np.percentile(X, lower), np.percentile(X, upper)), (0, 1))

    # potentially extend this to handle anistropic!
    def smooth_vol(self, vol_binary, ds=4, smooth=5):
        """
        Smooth an array with Gaussian filtering.

        :param vol_binary: np.array to smooth.
        :param ds: scale on which to apply the smoothing.
        :param smooth: Gaussian sigma to smooth data.
        :return: smoothed array.
        """
        from skimage.filters import gaussian
        from scipy.ndimage import gaussian_filter
        import skimage.transform as sktform
        import numpy as np

        small = sktform.resize(vol_binary, np.array(vol_binary.shape) // ds, preserve_range=True)
        small = gaussian_filter(small, sigma=smooth)

        return sktform.resize(small, np.array(vol_binary.shape), preserve_range=True)

    def anisodiff(self, img, niter=1, kappa=50, gamma=0.1, step=(1., 1.), sigma=0, option=1, ploton=False):
        """
        Anisotropic diffusion. Use as:
        imgout = anisodiff(im, niter, kappa, gamma, option)

        Kappa controls conduction as a function of gradient.  If kappa is low
        small intensity gradients are able to block conduction and hence diffusion
        across step edges.  A large value reduces the influence of intensity
        gradients on conduction. Gamma controls speed of diffusion (you usually want it at a maximum of
        0.25). Step is used to scale the gradients in case the spacing between adjacent
        pixels differs in the x and y axes. Diffusion equation 1 favours high contrast edges over low contrast ones.
        Diffusion equation 2 favours wide regions over smaller ones.

        Reference:
        P. Perona and J. Malik.
        Scale-space and edge detection using ansotropic diffusion.
        IEEE Transactions on Pattern Analysis and Machine Intelligence,
        12(7):629-639, July 1990.

        Original MATLAB code by Peter Kovesi
        School of Computer Science & Software Engineering
        The University of Western Australia
        pk @ csse uwa edu au
        <http://www.csse.uwa.edu.au>

        Translated to Python and optimised by Alistair Muldal
        Department of Pharmacology
        University of Oxford
        <alistair.muldal@pharm.ox.ac.uk>

        :param img: Input image
        :param niter: Number of iterations
        :param kappa: Conduction coefficient 20-100 ?
        :param gamma: Max value of .25 for stability
        :param step: Tuple, the distance between adjacent pixels in (y,x)
            option 1: Perona Malik diffusion equation No 1
            option 2: Perona Malik diffusion equation No 2
        :param ploton: - if True, the image will be plotted on every iteration
        :return: imgout   - diffused image.
        """

        # ...you could always diffuse each color channel independently if you
        # really want
        if img.ndim == 3:
            warnings.warn("Only grayscale images allowed, converting to 2D matrix")
            img = img.mean(2)

        # initialize output array
        img = img.astype('float32')
        imgout = img.copy()

        # initialize some internal variables
        deltaS = np.zeros_like(imgout)
        deltaE = deltaS.copy()
        NS = deltaS.copy()
        EW = deltaS.copy()
        gS = np.ones_like(imgout)
        gE = gS.copy()

        # create the plot figure, if requested
        if ploton:
            import pylab as pl
            from time import sleep

            fig = pl.figure(figsize=(20, 5.5), num="Anisotropic diffusion")
            ax1, ax2 = fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)

            ax1.imshow(img, interpolation='nearest')
            ih = ax2.imshow(imgout, interpolation='nearest', animated=True)
            ax1.set_title("Original image")
            ax2.set_title("Iteration 0")

            fig.canvas.draw()

        for ii in np.arange(1, niter):

            # calculate the diffs
            deltaS[:-1, :] = np.diff(imgout, axis=0)
            deltaE[:, :-1] = np.diff(imgout, axis=1)

            if 0 < sigma:
                deltaSf = flt.gaussian_filter(deltaS, sigma);
                deltaEf = flt.gaussian_filter(deltaE, sigma);
            else:
                deltaSf = deltaS;
                deltaEf = deltaE;

            # conduction gradients (only need to compute one per dim!)
            if option == 1:
                gS = np.exp(-(deltaSf / kappa) ** 2.) / step[0]
                gE = np.exp(-(deltaEf / kappa) ** 2.) / step[1]
            elif option == 2:
                gS = 1. / (1. + (deltaSf / kappa) ** 2.) / step[0]
                gE = 1. / (1. + (deltaEf / kappa) ** 2.) / step[1]

            # update matrices
            E = gE * deltaE
            S = gS * deltaS

            # subtract a copy that has been shifted 'North/West' by one
            # pixel. don't as questions. just do it. trust me.
            NS[:] = S
            EW[:] = E
            NS[1:, :] -= S[:-1, :]
            EW[:, 1:] -= E[:, :-1]

            # update the image
            imgout += gamma * (NS + EW)

            if ploton:
                iterstring = "Iteration %i" % (ii + 1)
                ih.set_data(imgout)
                ax2.set_title(iterstring)
                fig.canvas.draw()
            # sleep(0.01)

        return imgout

    def demix_videos(self, vid1, vid2, l1_ratio=0.5):
        """
        Spectrally unmix two arrays.

        :param vid1: np.array Stack 1 to unmix
        :param vid2: np.array Stack 2 to unmix
        :param l1_ratio: The regularization mixing parameter, with 0 <= l1_ratio <= 1.
            For l1_ratio = 0 the penalty is an elementwise L2 penalty (aka Frobenius Norm).
            For l1_ratio = 1 it is an elementwise L1 penalty.
            For 0 < l1_ratio < 1, the penalty is a combination of L1 and L2.
        :return: unmixed image in one stack
        """
        import numpy as np

        # vid = np.dstack([im[ref_slice], im_cancer[ref_slice]])
        vid = np.dstack([np.max(vid1, axis=0),
                         np.max(vid2, axis=0)])
        # vid = np.concatenate([im[...,None], im_cancer[...,None]], axis=-1)
        unmix_img, unmix_model = self.spectral_unmix_RGB(vid, n_components=2, alpha=1., l1_ratio=l1_ratio)
        mix_components = unmix_model.components_.copy()

        mix_components_origin = np.argmax(mix_components, axis=1)
        mix_components_origin_mag = np.max(mix_components, axis=1)

        mix_components_origin = mix_components_origin[mix_components_origin_mag > 0]

        NMF_channel_order = []
        NMF_select_channels = []
        select_channels = [0, 1]
        for ch in select_channels:
            if ch in mix_components_origin:
                # find the order.
                NMF_select_channels.append(ch)
                order = np.arange(len(mix_components_origin))[mix_components_origin == ch]
                NMF_channel_order.append(order)

        NMF_channel_order = np.hstack(NMF_channel_order)
        NMF_select_channels = np.hstack(NMF_select_channels)

        vid = np.concatenate([vid1[..., None],
                              vid2[..., None]], axis=-1)
        unmixed_vid = np.array([self.apply_unmix_model(frame, unmix_model) for frame in vid])

        # write this to a proper video.
        unmixed_vid_out = np.zeros_like(vid)
        unmixed_vid_out[..., NMF_select_channels] = unmixed_vid[..., NMF_channel_order]

        return unmixed_vid_out

    def apply_unmix_model(self, img, model):
        """
        Apply unmixing model on an image

        :param img: image to apply the unmixing to
        :param model: Unmixing model
        :return: unmixed image.
        """
        img_vector = img.reshape(-1, img.shape[-1]) / 255.
        img_proj_vector = model.transform(img_vector)

        img_proj_vector = img_proj_vector.reshape((img.shape[0], img.shape[1], -1))
        # img_proj_vector = np.uint8(255*rescale_intensity(img_proj_vector))

        return img_proj_vector

    def spectral_unmix_RGB(self, img, n_components=3, l1_ratio=0.5):
        """
        Spectral unmixing function using Non-Negative Matrix Factorization.

        :param img: Stack of all combined images to unmix (e.g. combine two images:
            vid = np.dstack([np.max(vid1, axis=0), np.max(vid2, axis=0)])
        :param n_components: how many images/components there are
        :param l1_ratio: The regularization mixing parameter, with 0 <= l1_ratio <= 1.
            For l1_ratio = 0 the penalty is an elementwise L2 penalty (aka Frobenius Norm).
            For l1_ratio = 1 it is an elementwise L1 penalty.
        :return: unmixed image stack, unmix color model
        """
        from sklearn.decomposition import NMF
        from skimage.exposure import rescale_intensity

        img_vector = img.reshape(-1, img.shape[-1]) / 255.
        #    img_vector = img_vector_.copy()itakura-saito
        #    img_vector[img_vector<0] = 0
        # nndsvd, nndsvda, nndsvdar
        color_model = NMF(n_components=n_components, init='nndsvda', random_state=0,
                          l1_ratio=l1_ratio)  # Note ! we need a high alpha ->.
        W = color_model.fit_transform(img_vector)

        print(W.shape)
        img_vector_NMF_rgb = W.reshape((img.shape[0], img.shape[1], -1))
        img_vector_NMF_rgb = np.uint8(255 * rescale_intensity(img_vector_NMF_rgb))

        #    # get the same order of channels as previous using the model components.
        #    channel_order = np.argmax(color_model.components_, axis=0);
        #    print(channel_order)
        #    img_vector_NMF_rgb = img_vector_NMF_rgb[...,channel_order]

        # return the color model.
        return img_vector_NMF_rgb, color_model





