import signal
import ee
import math


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

    def __init__(self, crs=None, scale=None, crsTransform=None):
        """init crs."""
        super(CRS, self).__init__()

        self.set_crs(crs)
        self.set_scale(scale)
        self.set_crsTransform(crsTransform)

    def set_crs(self, crs):
        """setter."""
        self.crs = crs

    def set_scale(self, scale):
        """setter."""
        self.scale = scale

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
        if self.crs is None:
            print('crs not defined')
            raise Exception('exit')

        status_scale = self.scale is None
        status_crsTransform = self.crsTransform is None

        if status_scale == status_crsTransform:
            print('scale/crsTransform problem')
            raise Exception('exit')

    def __call__(self):
        """
        get crs dictionary.
        crs dictionary is one of the following pairs
            {crs, scale}
            {crs, crsTransform}
        """
        self.validate_crs()

        dic = self.__dict__
        out = {}
        for entry in dic:
            if dic[entry] is not None:
                out[entry] = dic[entry]

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
