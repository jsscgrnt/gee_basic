import ee
import sys

import socket
print('current computer:', socket.gethostname())

if socket.gethostname() == 'sentinel2':
    sys.path.append('/home/rviegas/Dropbox')
    sys.path.append('/media/data/sao_domingos_de_prata/config_donwload_sentinel')
elif socket.gethostname() == 'instance-1':
    sys.path.append('/home/rviegas/')
else:
    print 'Unknown computer!'
    raise Exception('exit')

from gee_basic import exporter, Task, basic
import config
# check argparse, for future versions

basic.cwa(ee.Initialize)

crs_descriptor = basic.CRS(
    crs=config.crs,
    scale=config.scale
)

if config.geometry is not None:
    config.geometry = ee.FeatureCollection(config.geometry)

tasks = {}
granule = config.granules[0]
for granule in config.granules:

    collection = ee.ImageCollection('COPERNICUS/S2')\
        .filterMetadata('MGRS_TILE', 'equals', granule)\
        .filterDate(config.start_date, config.end_date)

    info = basic.cwa(collection.getInfo)
    info = info['features']
    info = [i['id'] for i in info]

    for ID in info:

        # Load image, make it Int 16  and select desired bands
        img = ee.Image(ID)
        img = img.toInt16()
        img = img.select(config.desired_bands)
        if config.geometry is not None:
            geo = ee.Feature(config.geometry.first()).geometry()
            geo = img.geometry().intersection(geo)
            img = img.clip(geo)

        # Make out image name
        # ID =  u'COPERNICUS/S2/20180404T130251_20180404T130247_T23KQU'
        dummy = ID.split('/')
        dummy = dummy[len(dummy) - 1]
        date = dummy[0:8]
        name = '_'.join(['SEN2', date,  granule])

        info = {
            'image': img,
            'task_id': name,
            'crs': crs_descriptor,
            'folder': config.folder
        }

        t = Task.image_task(**info)
        tasks[name] = t
        print name


taskControl = {'log': []}

imgs = tasks.keys()
imgs.sort()

for name in imgs:

    while len(taskControl) == 10:
        taskControl = exporter.check_exports(taskControl).check()

    print ('starting: ', name)

    t = tasks[name]
    t.gee_task.start()
    taskControl[name] = t

while len(taskControl) > 1:
    taskControl = exporter.check_exports(taskControl).check()
