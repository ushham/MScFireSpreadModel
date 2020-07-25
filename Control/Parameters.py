from datetime import datetime

#Basic parameters
coord1 = (-12.1483, 142.2290)
coord2 = (-12.3459, 142.4864)

xsize = 400
ysize = 400

datesin = ['2019-11-11', '2019-11-12', '2019-11-13', '2019-11-14', '2019-11-15', '2019-11-16', '2019-11-17']

saveloc = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Outputs\North QLD'

#FileLocations
waterfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Surface Water\EU Database\150E-20S'
waterfile = 'seasonality_150E_20S_v1_1.tif'

elefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\Australia'
elefile = '30S120E_20101117_gmted_mea075.tif'

firefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\FireData\Aus\Aus 20191123 VIIRS'
firefile = 'fire_nrt_V1_88533.shp'

weatherfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\GRIB\20-11 Aus'
weatherfile = 'adaptor.mars.internal-1595605290.199956-21027-5-86639461-543b-414f-b0ee-ae8c3230580b.grib'

#Fire Data
hrspace = 12
dt = datetime(2019, 11, 11, 0, 0)
startcoords = (-8, 112)

#Windspeed/hill length interaction
windhill = 8 / 5
upperwindlim = 10

#CA Parameters
k = 10          #number of CA states
ell = 10000       #number of trials for Transition matrix

delx = 1        #size of step
delt = 0.08     #size of time step
vee = 0.5       #spread constant
kapa = 0.8      #growth constant

#array sizes
n = ysize
m = xsize
t = 10