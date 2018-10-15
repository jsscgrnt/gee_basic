import signal
import math
from gee_basic import ee


class TimeoutException(Exception):
    """Custom exception class."""

    pass


def timeout_handler(signum, frame):
    """
    Customise signal handling.
    """

    raise TimeoutException


signal.signal(signal.SIGALRM, timeout_handler)


def cwa(func):
    """
    cwa = communication_with_alarm.
    Run function with an alarm so that the program do not get stuck.
    """
    while True:
        signal.alarm(30)
        try:
            dummy = func()
            break
        except(KeyboardInterrupt):
            signal.alarm(0)
            raise
        except TimeoutException:
            print('~~timeout~~')
        except Exception as e:
            print(e)
    signal.alarm(0)
    return dummy


def cancelGEETasks(number=None):
    """
    cancelando as imagens que etavam na fila para serem geradas.
    """

    end = 10

    if number is not None:
        end = number

    batch_list = ee.batch.Task.list()
    fckingList = batch_list[0:end]

    for i in fckingList:
        print i.config
        i.cancel()


class CRS(object):
    """docstring for CRS."""

    def __init__(self, epsg=None, scale=None, crsTransform=None):
        """init crs."""
        super(CRS, self).__init__()

        self.set_epsg(epsg)
        self.set_scale(scale)
        self.set_crsTransform(crsTransform)

    def set_epsg(self, epsg):
        """setter."""
        self.epsg = epsg

    def set_scale(self, scale):
        """setter."""
        self.scale = scale

    def set_crsTransform_from_dic(self, dic, tile):
        """setter."""

        crsTransform = [
            dic['pixel_sizeX'][tile],
            0,
            dic['originX'][tile],
            0,
            dic['pixel_sizeY'][tile],
            dic['originY'][tile]
        ]

        self.set_crsTransform(crsTransform)

    def set_crsTransform(self, crsTransform):
        """setter."""
        self.crsTransform = crsTransform

    def validate_crs(self):
        """
        makes sure if the crs object mekes sense.
        checks if crs is no None
        checks if scale and crsTransform are not both None
        or if both are set
        """
        if self.epsg is None:
            print('crs not defined')
            raise Exception('exit')

    def get_crs_and_scale(self):
        """
        get crs dictionary.
        crs dictionary is one of the following pairs
            {crs, scale}
            {crs, crsTransform}
        """
        self.validate_crs()

        dic = self.__dict__
        out = {
            'crs': dic['epsg'],
            'scale': dic['scale']
        }
        return out

    def get_crs_and_crsTransform(self):
        """
        get crs dictionary.
        crs dictionary is one of the following pairs
            {crs, scale}
            {crs, crsTransform}
        """
        self.validate_crs()

        dic = self.__dict__
        out = {
            'crs': dic['epsg'],
            'crsTransform': dic['crsTransform']
        }
        return out


def getQABits(image, start, end):
    pattern = 0
    for i in xrange(start, end + 1):
        pattern = pattern + math.pow(2, i)
    return image.select([0]).bitwiseAnd(int(pattern)).rightShift(start)


def clear_landsat(image):
    QA = image.select(['pixel_qa'])
    qa_value = getQABits(QA, 1, 1)
    qa_value = qa_value.select([0], ['BQA'])

    return qa_value


def rescale(img, exp, thresholds):
    bands = [
        'B1', 'B2', 'B3', 'B4',
        'B5', 'B6', 'B7', 'B8', 'B8A',
        'B9', 'B10', 'B11', 'B12'
    ]
    dic_bands = {i: img.select(i) for i in bands}

    if exp == 'img':
        # print 'hi'
        out = img.subtract(thresholds[0])\
            .divide(thresholds[1] - thresholds[0])
    else:
        out = img.expression(exp, dic_bands)\
            .subtract(thresholds[0]).divide(thresholds[1] - thresholds[0])
    return out


def sentinelCloudScore(image):
    bands = [
        'B1', 'B2', 'B3', 'B4',
        'B5', 'B6', 'B7', 'B8', 'B8A',
        'B9', 'B10', 'B11', 'B12'
    ]

    img = image.select(bands).divide(10000)  # Rescale to 0-1

    # Compute several indicators of cloudyness and take the minimum of them.
    score = ee.Image(1)

    # Clouds are reasonably bright in the blue and cirrus bands.
    score = score.min(rescale(img, 'B2', [0.1, 0.5]))
    score = score.min(rescale(img, 'B1', [0.1, 0.3]))
    score = score.min(rescale(img, 'B1 + B10', [0.15, 0.2]))

    # Clouds are reasonably bright in all visible bands.
    score = score.min(rescale(img, 'B4 + B3 + B2', [0.2, 0.8]))

    # Clouds are moist
    ndmi = img.normalizedDifference(['B8', 'B11'])
    score = score.min(rescale(ndmi, 'img', [-0.1, 0.1]))

    # However, clouds are not snow.
    ndsi = img.normalizedDifference(['B3', 'B11'])
    score = score.min(rescale(ndsi, 'img', [0.8, 0.6]))

    score = score.multiply(100).byte()

    return score


def clear_sentinel(image):

    cs = sentinelCloudScore(image)
    cs = cs.lte(10)
    k = ee.Kernel.fixed(5, 5,
                        [
                            [1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1]
                        ]
                        )

    buff = cs.focal_min(kernel=k, iterations=10)
    qa = cs.addBands(buff).select([0, 1], ['BQA', 'Bbuff'])

    return qa
