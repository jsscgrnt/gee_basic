from gee_basic import ee
from gee_basic import cwa


class eeFeatureCollection(object):
    """
    Class that handles ee.FeatureCollection creations and operations.
    """

    def __init__(self, fc, length=None, fusion_table=False):
        """
        Prepare eeFeatureCollection and recover it's length.

        # attributes

        self.eeFeatureCollection = None
        self.id = None
        """

        self.fc = fc
        self.fusion_table = fusion_table
        self.length = length
        self.set_eeFeatureCollection()

    def set_eeFeatureCollection(self):
        """
        Set eeFeatureCollection according with it's type.
        """

        if type(self.fc).__name__ == 'FeatureCollection':
            self.eeFeatureCollection = self.fc

        elif type(self.fc).__name__ == 'str':

            self.fc = self.fc
            self.id = self.fc
            if self.fusion_table:
                self.id = 'ft:' + self.fc

            self.eeFeatureCollection = ee.FeatureCollection(
                self.id
            )

        else:
            print self.fc, type(self.fc).__name__
            print('not implemented,  fc unknown')
            raise Exception('exit')

        self.set_feature_collection_length(self.length)

    def set_feature_collection_length(self, length=None):
        """
        Set eeFeatureCollection length.
        If not informed a getInfo will be used to recover it.
        """

        self.length = length

        if self.length is None:

            fc_size_GEE = self().size()
            fc_size = cwa(
                fc_size_GEE.getInfo
            )

            self.length = fc_size

    def slicer(self, start, step):
        """
        Slice eeFeatureCollection, returns a new eeFeatureCollection object.
        Fails if feature collection length is bigger than 5000, not sure (?)
        """

        fc_list = self().toList(step, start)
        fc = ee.FeatureCollection(fc_list)

        out = eeFeatureCollection(fc, length=step)

        return out

    def filterBounds(self, geometry):
        """
        Filter featureCollection by a geometry, living only the features
        that are within the geometry
        """

        dummy = self().filterBounds(geometry)

        return eeFeatureCollection(dummy)

    def __call__(self):

        return self.eeFeatureCollection
