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
import config_landsat as config
# check argparse, for future versions


def make_name_out(i):

    # ID =  u'COPERNICUS/S2/20180404T130251_20180404T130247_T23KQU'
    dummy = i['id'].split('/')
    dummy = dummy[len(dummy) - 1]
    dummy = dummy.split('_')
    date = dummy[2]
    tile = dummy[1]
    spacecraft = dummy[0]

    cc = str(int(i['properties']['CLOUD_COVER']))

    sat = i['properties']['SATELLITE'].split('_')[1]
    bands = [k[1:] for k in config.desired_bands[sat]]
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

if config.qa:
    print 'Exporting QA as band 4'
    config.desired_bands = {
        i: config.desired_bands[i] + ['BQA']
        for i in config.desired_bands
    }

tasks = {}

collections = {
    '8': 'LANDSAT/LC08/C01/T1_SR',
    '7': 'LANDSAT/LE07/C01/T1_SR',
    '5': 'LANDSAT/LT05/C01/T1_SR'
}

if config.tiles != config.images:
    images_info = []

    if config.images is None:
        print('List of TILES informed')
        # tile = config.tiles[0]
        # ck = collections[0]
        for ck in collections:
            for tile in config.tiles:
                collection = ee.ImageCollection(collections[ck])\
                    .filterMetadata('WRS_PATH', 'equals', int(tile[:3]))\
                    .filterMetadata('WRS_ROW', 'equals', int(tile[3:]))\
                    .filterDate(config.start_date, config.end_date)

                info = basic.cwa(collection.getInfo)
                info = info['features']
                for i in info:
                    i['desired_bands'] = config.desired_bands[ck]
                images_info = images_info + info

    elif config.tiles is None:

        collections = {collections[i]: i for i in collections}

        for i in config.images:
            dummy = i.split('/')
            ck = '/'.join(dummy[:(len(dummy) - 1)])

            img = ee.Image(i)
            info = basic.cwa(img.getInfo)
            info['desired_bands'] = config.desired_bands[collections[ck]]
            images_info.append(info)

    else:

        print 'Something is wrong with the config file, check IMAGES and TILES'
        raise Exception('exit')

else:

    print 'Something is wrong with the config file, check IMAGES and TILES'
    raise Exception('exit')


for i in images_info:

    # Load image, make it Int 16  and select desired bands
    img = ee.Image(i['id'])

    if config.qa:
        qa = basic.clear_landsat(img)
        img = img.addBands(qa)

    img = img.toInt16()
    img = img.select(i['desired_bands'])
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
