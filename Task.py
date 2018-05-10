from gee_basic import ee
from gee_basic import cwa


class image_task(object):
    """docstring for task."""

    def __init__(self, image=None, task_id=None, crs=None, folder=None):
        """
        Do everything that should be done.
        """
        super(image_task, self).__init__()
        self.no_valid_pixels_msg = 'Export region contains no valid (un-masked) pixels.'
        self.max_pixels = 1E13

        self.set_image(image)
        self.set_crs(crs)
        self.set_task_id(task_id)
        self.set_export_folder(folder)

        if self.folder is not None:
            self.export_to_drive()

    def set_export_folder(self, folder):
        """
        set export folder
        """
        self.folder = folder

    def set_image(self, image):
        """
        Do everything that should be done.
        """
        self.image = image

    def set_crs(self, crs):
        """
        Do everything that should be done.
        """
        self.crs = crs

    def set_task_id(self, task_id):
        """
        Do everything that should be done.
        """
        self.task_id = task_id

    def validate(self):

        for x in [self.image, self.crs, self.task_id, self.folder]:
            if x is None:
                print 'image/crs/task_id/folder not informed'
                print 'image: ', self.image
                print 'crs: ', self.crs
                print 'task_id: ', self.task_id
                print 'folder: ', self.folder
                raise Exception('exit')

    def export_to_drive(self, folder=None):
        """
        Do everything that should be done.
        """

        if folder is not None:
            self.folder = folder

        self.validate()

        gee_task = ee.batch.Export.image.toDrive(
            self.image,
            description=self.task_id,
            folder=self.folder,
            fileNamePrefix=self.task_id,
            maxPixels=self.max_pixels,
            **self.crs()
        )
        self.gee_task = gee_task

    def check_status(self):
        """
        Do everything that should be done.
        """
        self.load()
        self.handle_state()

    def get_status(self):
        """
        Does a getInfo the best known way.
        """
        self.status = cwa(self.gee_task.status)

    def set_infos(self):
        """
        Set some basic infos.
        """
        self.state = self.status['state']

    def load(self):
        """
        Pull task information from GEE servers.
        """
        self.get_status()
        self.set_infos()

    def handle_state(self):
        """
        If self.flag then then task is ready to be removed from taskControl.
        Note that self.flag will be True if task's state equals one
        of the following:
        >COMPLETED
        >CANCELLED
        >FAILED
        """

        if self.state in ('RUNNING', 'READY'):
            self.msg = '\n'.join(
                [self.task_id, self.state]
            )

            self.flag = False

        else:

            self.flag = True

            if self.state == 'COMPLETED':
                self.msg = '\n'.join(
                    [
                        self.task_id,
                        'completed and removed from taskControl, congrats'
                    ]
                )

            elif self.state == 'CANCELLED':
                self.msg = '\n'.join(
                    [self.task_id, self.state]
                )

            elif self.state == 'FAILED':
                if self.status['error_message'] == self.no_valid_pixels_msg:
                    self.msg = '\n'.join(
                        [self.task_id, '==> EMPTY TILE | no valid pixels']
                    )
                else:
                    self.msg = '\n'.join(
                        [
                            self.state,
                            self.task_id,
                            self.status['error_message']
                        ]
                    )
