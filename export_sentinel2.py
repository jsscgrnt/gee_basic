import ee
import sys

import socket
print('current computer:', socket.gethostname())

if socket.gethostname() == 'sentinel2':
    sys.path.append('/home/rviegas/Dropbox')
elif socket.gethostname() == 'instance-1':
    sys.path.append('/home/rviegas/')
else:
    print 'Unknown computer!'
    raise Exception('exit')

from gee_basic import exporter, Task, basic

sys.path.append(sys.argv[1])
import config_sentinel2 as config
# check argparse, for future versions


def make_name_out(i):
    # ID =  u'COPERNICUS/S2/20180404T130251_20180404T130247_T23KQU'
    dummy = i['id'].split('/')
    dummy = dummy[len(dummy) - 1]
    dummy = dummy.split('_')
    date = dummy[0][0:8]
    tile = dummy[len(dummy) - 1]

    spacecraft = 'S2' + i['properties']['SPACECRAFT_NAME'][10:]

    cc = str(int(i['properties']['CLOUDY_PIXEL_PERCENTAGE']))

    bands = [k[1:] for k in config.desired_bands]
    bands = ''.join(bands)

    name = '_'.join([spacecraft, date,  tile, bands, cc])

    return name


basic.cwa(ee.Initialize)

crs_descriptor = basic.CRS(
    crs=config.crs,
    scale=config.scale
)

if config.geometry is not None:
    config.geometry = ee.FeatureCollection(config.geometry)
    config.geometry = ee.Feature(config.geometry.first()).geometry()
    if config.geometry_buff is not None:
        config.geometry = config.geometry.buffer(config.geometry_buff)

tasks = {}

if config.tiles != config.images:
    images_info = []

    if config.images is None:
        print('List of TILES informed')
        tile = config.tiles[0]
        for tile in config.tiles:
            collection = ee.ImageCollection('COPERNICUS/S2')\
                .filterMetadata('MGRS_TILE', 'equals', tile)\
                .filterDate(config.start_date, config.end_date)

            info = basic.cwa(collection.getInfo)
            info = info['features']
            images_info = images_info + info

    elif config.tiles is None:
        print('List of IMAGES informed')
        for i in config.images:
            img = ee.Image(i)
            images_info.append(basic.cwa(img.getInfo))

    else:

        print 'Something is wrong with the config file, check IMAGES and TILES'
        raise Exception('exit')

else:

    print 'Something is wrong with the config file, check IMAGES and TILES'
    raise Exception('exit')


for i in images_info:

    # Load image, make it Int 16  and select desired bands
    img = ee.Image(i['id'])
    img = img.toInt16()
    img = img.select(config.desired_bands)
    if config.geometry is not None:
        geo = img.geometry().intersection(config.geometry)
        img = img.clip(geo)

    # Make image name
    name = make_name_out(i)

    INFO = {
        'image': img,
        'task_id': name,
        'crs': crs_descriptor,
        'folder': config.folder
    }

    t = Task.image_task(**INFO)
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
