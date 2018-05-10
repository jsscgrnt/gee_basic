

class Extractor(object):
    """
    Docstring.
    """

    def __init__(self, eeimage, fc, step, scale, crs, check_var, na_value=None):
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
        self.crs = crs
        self.check_var = check_var
        self.na_value = na_value

    def extract_values(self):
        """
        Docstrinf.
        ev = Extracted Values
        """

        def recover_info(info):
            """
            Docsrtring.
            """

            info = info.getInfo
            info = cwa(info)

            if self.check_var not in info['features'][0]['properties'].keys():
                print('Unknown check_var')
                raise Exception('exit')

            ev = [
                i['properties']
                for i in info['features']
                if i['properties'][self.check_var] not in [None, self.na_value]
            ]

            ev = self.add_image_id(ev)

            return ev

        ev = []

        image = self.eeimage()
        number_of_iterations = (self.fc.length / self.step) + 1
        str_number_of_iterations = str((self.fc.length / self.step) + 1)

        for i in xrange(0, number_of_iterations):

            print(' / '.join([str(i + 1), str_number_of_iterations]))

            info = self.gee_extraction(i, image)
            ev = ev + recover_info(info)

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
            self.scale,
            self.crs,
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
