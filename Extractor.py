

class Extractor(object):
    """
    Docstring.
    """

    def __init__(self, eeimage, fc, step, scale):
        """
        Docstring.

        # attributes

        self.image
        self.fc
        self.step
        self.scale
        """

        self.eeimage = eeimage
        self.fc = fc
        self.step = step
        self.scale = scale

    def extract_values(self, check_var):
        """
        Docstrinf.
        ev = Extracted Values
        """

        def recover_info(info, check_var):
            """
            Docsrtring.
            """

            info = info.getInfo
            info = cwa(info)

            ev = [
                i['properties']
                for i in info['features']
                if i['properties'][check_var] is not None
            ]
            ev = self.add_image_id(ev)

            return ev

        ev = []

        image = self.eeimage.image
        steps = str((self.fc.length / self.step) + 1)

        for i in xrange(0, (self.fc.length / self.step) + 1):

            print(' / '.join([str(i), steps]))

            info = self.gee_extraction(i, image)
            ev = ev + recover_info(info, check_var)

        return ev

    def gee_extraction(self, i, image):
        """
        Docstring.
        """

        fc = self.slice(i)

        # print fc.getInfo()

        info = image.reduceRegions(
            fc,
            ee.Reducer.mean(),
            20,
            'EPSG:29193',
            # [30.011725000000006, 0, 224526.069712127937237,
            #     0, -30.011725000000002, 9529699.013013089075685]
        )

        # pdb.set_trace()

        return info

    def slice(self, i):
        """
        Docstring.
        """

        fc0 = self.fc
        fc_slice = fc0.slicer(self.step * i, self.step)
        fc = fc_slice.eeFeatureCollection

        # pdb.set_trace()

        return fc

    def add_image_id(self, ev):
        """
        Docstring.
        """

        for i in ev:
            dummy = i
            dummy['image_id'] = self.eeimage.id

        return ev
