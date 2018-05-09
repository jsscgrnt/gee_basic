# import ee
# needs ee


class glcmCalculator(object):
    """
    Docstring.
    """

    def __init__(self, eeImage, info):
        """
        Docstring.
        info is a dictionary with the band name and its multiplication value
        glcm will only be computed for the bands that are in info
        """

        self.eeImage = eeImage
        self.info = info

    def calc_glcm(self):
        """
        Note that the image will be converted to int, so variables with small
        range shall have some problems.
        """

        img = []

        for band in self.info:

            dummy = self.eeImage.bands_dic[band]

            if self.info[band] not in [1, None]:

                dummy = dummy.multiply(self.info[band])

            img.append(dummy)

        image = ee.Image(img)
        image = image.toInt()
        glcm_image = image.glcmTexture()

        return glcm_image

    def glcm_bands_names(self):
        """
        Docstring.
        """

        glcms = ['asm', 'contrast', 'corr', 'var', 'idm',
                 'savg', 'svar', 'sent', 'ent', 'dvar',
                 'dent', 'imcorr1', 'imcorr2', 'maxcorr',
                 'diss', 'inertia', 'shade', 'prom']

        band_names = []
        for band in self.info:
            for glcm in glcms:
                dummy = '_'.join([band, glcm])
                band_names.append(dummy)

        return band_names

    def calc(self):
        """
        Docstring.
        """

        image = self.calc_glcm()
        bands = self.glcm_bands_names()

        self.eeImage.update(image, bands)

        return self.eeImage
