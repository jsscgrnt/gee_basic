

class eeImage(object):
    """
    Class that handles ee.Images creations.

    # attributes

        self.refactor_cst = None
        self.image = None
        self.id = None
        self.bands_dic = None
        self.bands = None
    """

    def __init__(
        self,
        image,
        bands=None,
        rename_bands=False,
        to_int=False,
        mask=None
    ):
        """
        Init method. Defines image acording to the input.
        bands is a list of strings (bands names).
        refactor_cst is None if the image is not refactored
        """

        self.mask = {'mask': mask, 'already_aplied': False}
        self.set_image(image, to_int)
        self.set_image_bands(bands, rename_bands)

    def set_image(self, image, to_int):
        """
        Set image acording to it's type.
        """

        if type(image).__name__ == 'Image':
            self.id = 'there is no easy id for me, you can call me babe'
            self.image = image

        elif type(image).__name__ == 'str':
            self.id = image
            self.image = ee.Image(self.id)

        else:
            print image, type(image).__name__

        if to_int:
            self.image = self.image.toInt()

        self.mask_image()
        self.set_name()

    def mask_image(self):
        """
        Docstring.
        """

        if self.mask['already_aplied']:
            if self.mask['mask'] is not None:
                self.image = self.image.updateMask(self.mask['mask'])

    def update(self, image, new_bands=None):
        """
        Update image.
        If new bands is not informed then a getInfo is used to
        get the new bands and the miethod is called again.
        If new bands is informed, than it is appended to the self.bands,...
        """

        if new_bands is not None:
            self.image = self.image.addBands(image)
            self.append_bands_list(new_bands)

        else:
            image_info = cwa(image.getInfo)
            image_bands_info = image_info['bands']
            new_bands = [
                band['id'] for band in image_bands_info
                if band['id'] not in self.bands
            ]

            self.update(image, new_bands)

    def append_bands_list(self, new_bands):
        """
        Append new bands to the self.bands.
        Make it so that the self.band_dic is updated.
        """

        if type(new_bands).__name__ == 'str':
            new_bands = [new_bands]

        self.bands = self.bands + new_bands

        self.make_bands_dictionary(new_bands)

    def set_image_bands(self, bands, rename_bands):
        """
        Set image bands and computes bands_dic.
        If bands_list == None than a a getInfo is used to recover bands names.
        Rename bands if True, note that bands_list == None
        is mutually exclusive with rename_bands.
        """

        if bands is None:
            dummy = self.image
            dummy = cwa(dummy.getInfo)
            bands = [band['id'] for band in dummy['bands']]

        elif rename_bands:
            self.rename_bands(bands)

        self.bands = bands

        self.make_bands_dictionary()

    def rename_bands(self, bands):
        """
        Rename bands.
        Currently, assumes that all band are being renamed.
        Could be improved
        """

        rng = range(0, len(bands))
        self.image = self.image.select(rng, bands)

    def make_bands_dictionary(self, new_bands=None):
        """
        Make or update self.band_dic.
        If new_bands == None, cleans the bands_dic, than computes it again,
        Otherwise only appends to the self,bands_dic the new band(s).
        """

        if new_bands is None:
            self.bands_dic = {}

            for band in self.bands:
                self.bands_dic[band] = self.image.select(band)

        else:
            for band in new_bands:
                self.bands_dic[band] = self.image.select(band)

    def refactor_image_values(self, cst):
        """
        Multiply image by a constant.
        """

        self.refactor_cst = cst
        self.image = self.image.multiply(cst)

    def set_name(self):
        """
        Set image name out.
        """
        if '/' in self.id:
            name = self.id.split('/')
            name = name[len(name) - 1]
            self.name = name + '_desiredVars'
        else:
            print('not able to define name for this image')
            raise Exception('exit')
