# ARQUIVO DE CONFIGURACAO PARA EXPORTAR IMAGENS SENTINEL 2
# PARA O GOOGLE DRIVE, UTLIZANDO O GOOGLE EARTH ENGINE.

# DATAS
# start_date - data inicial para procurar imagens
# exemplo: start_date = '2013-05-01'
start_date = '2013-05-01'
# end_date - ultima data para procurar imagens
# exemplo: end_date = '2018-12-01'
end_date = '2018-12-01'
# OBS: (I) end_date pode ser uma data que ainda nao aconteceu
#      (II) datas impossiveis nao funcionam, e.g, '2018-05-31'

# CRS
# codigo EPSG (escrever EPSG maiusculo), ver http://spatialreference.org/
# exemplo: crs = 'EPSG:4326'
crs = 'EPSG:4326'

# TAMANHO DO PIXEL
# tamanho que o pixel da imagem de saida vai ter
# exemplo: scale = 20
scale = 20

# TILES SENTINEL
# tiles para serem exportados
# os possiveis valores sao:
# uma lista de strings: ['granule1','granule2',...,'granuleN']*
# ou None, ver **
# # exemplo: tiles = [
# #     '23KPT',
# #     '23KPU',
# #     '23KQT',
# #     '23KQU'
# # ]
# tiles = None
tiles = [
    '23KPT',
    '23KPU',
    '23KQT',
    '23KQU'
]
# caso se saiba apriori quais imagens devem ser exportadas,
# as imagens podem ser informadas como um lista de strings ver *
# note que se 'images' e 'tiles' sao mutualmente exclusivos**.
# entao se tiles for uma lista de strings, entao images=None
# ou vice e versa, caso contrario teremos um erro.
# exemplo: images = [
#     'COPERNICUS/S2/20160713T130431_20160713T192011_T23KPT',
#     'COPERNICUS/S2/20160713T130431_20160713T192011_T23KPU'
# ] ou images = None
# images = [
#     'COPERNICUS/S2/20160713T130431_20160713T192011_T23KPT',
#     'COPERNICUS/S2/20160713T130431_20160713T192011_T23KPU',
#     'COPERNICUS/S2/20160713T130431_20160713T192011_T23KQT',
#     'COPERNICUS/S2/20160713T130431_20160713T192011_T23KQU',
#     'COPERNICUS/S2/20160802T130656_20160802T193908_T23KPU',
#     'COPERNICUS/S2/20170330T130241_20170330T130532_T23KPT',
#     'COPERNICUS/S2/20170723T130249_20170723T130633_T23KQT',
#     'COPERNICUS/S2/20170723T130249_20170723T130633_T23KQU',
#     'COPERNICUS/S2/20170817T130251_20170817T130509_T23KPT',
#     'COPERNICUS/S2/20170817T130251_20170817T130509_T23KPU',
#     'COPERNICUS/S2/20170817T130251_20170817T130509_T23KQU'
# ]
images = None

# GEOMETRIA
# geometria para cortar todos os tiles, polygon nao multipolygons
# se geometry=None, entao o tile inteiro sera exportado
# exemplo: geometry = 'users/cnp_rafael/buffer_50km'
geometry = 'users/cnp_rafael/buffer_50km'

# GEOMETRY BUFFER
geometry_buff = 5000

# PASTA DE SAIDA
# nome da pasta para qual as imagens vao ser exportadas
# exemplo: folder_name = 'sao_domingos_do_prata'
folder = 'sao_domingos_SELECTED'

# DESIRED BANDS
# informe as bandas desejadas no formato de lista de strings ver *
# ver https://landsat.gsfc.nasa.gov/sentinel-2a-launches-our-compliments-our-complements/
# exemplo: desired_bands = ['B8A', 'B11', 'B4']
desired_bands = ['B8A', 'B11', 'B4']
