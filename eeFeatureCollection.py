

class eeFeatureCollection(object):
    """
    Class that handles ee.FeatureCollection creations and operations.
    """

    def __init__(self, fc, length=None, fusion_table=False):
        """
        Prepare eeFeatureCollection and recover it's length.

        # attributes

        self.eeFeatureCollection = None
        self.fusion_table = None
        self.id = None
        self.length = None
        """

        self.set_eeFeatureCollection(fc, fusion_table)
        self.set_feature_collection_length(length)

    def set_eeFeatureCollection(self, fc, fusion_table):
        """
        Set eeFeatureCollection according with it's type.
        """

        if type(fc).__name__ == 'FeatureCollection':
            self.eeFeatureCollection = fc

        elif type(fc).__name__ == 'str':

            if fusion_table:
                fc = 'ft:' + fc
                self.fusion_table = fusion_table

            self.id = fc
            self.eeFeatureCollection = ee.FeatureCollection(
                self.id
            )

        else:
            print fc, type(fc).__name__

    def set_feature_collection_length(self, length):
        """
        Set eeFeatureCollection length.
        If not informed a getInfo will be used to recover it.
        """

        self.length = length

        if length is None:

            fc = self.eeFeatureCollection
            fc_size_GEE = fc.size()
            fc_size = cwa(
                fc_size_GEE.getInfo
            )

            self.length = fc_size

    def slicer(self, start, step):
        """
        Slice eeFeatureCollection, returns a new eeFeatureCollection object.
        Fails if feature collection length is bigger than 5000, not sure (?)
        """

        fc0 = self.eeFeatureCollection
        fc_list = fc0.toList(step, start)
        fc = ee.FeatureCollection(fc_list)

        out = eeFeatureCollection(fc, length=step)

        return out
