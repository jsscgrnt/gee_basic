import time


def sleep():

    print 'sleep ...',
    time.sleep(4)
    print ' wake'


class check_exports(object):
    """docstring for check_exports."""

    def __init__(self, tc):
        super(check_exports, self).__init__()
        self.taskControl = dict(tc)
        self.division = "#####################################" + '\n'

        self.get_keys()
        self.msg = None

    def get_keys(self):
        keys = self.taskControl.keys()
        # import pdb
        # pdb.set_trace()
        if 'log' in keys:
            keys.remove('log')
        self.keys = keys

    def check(self):

        for task_key in self.keys:
            task = self.taskControl[task_key]

            task.check_status()
            print task.msg
            if task.flag:
                del self.taskControl[task_key]
                self.taskControl['log'].append(task.msg)
                break

        sleep()

        print '\n' + self.division
        return self.taskControl
