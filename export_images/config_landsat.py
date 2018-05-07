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
scale = 30

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
    '217074'
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
#     'LANDSAT/LC08/C01/T1_SR/LC08_217074_20130802',
#     'LANDSAT/LC08/C01/T1_SR/LC08_217074_20140805',
#     'LANDSAT/LC08/C01/T1_SR/LC08_217074_20150925',
#     'LANDSAT/LC08/C01/T1_SR/LC08_217074_20160810',
#     'LANDSAT/LC08/C01/T1_SR/LC08_217074_20180120'
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
folder = 'sao_domingos_all'

# DESIRED BANDS
# informe as bandas desejadas no formato de lista de strings ver *
# ver https://landsat.gsfc.nasa.gov/sentinel-2a-launches-our-compliments-our-complements/
# exemplo: desired_bands = ['B8A', 'B11', 'B4']
desired_bands = {
    '8': ['B5', 'B6', 'B4'],
    '7': ['B4', 'B5', 'B3'],
    '5': ['B4', 'B5', 'B3']
}

# BANDA DE QUALIDADE
# Se true, a banda de qualidade no formato binario tambem vai ser exportada
qa = True
