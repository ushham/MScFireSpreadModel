from datetime import datetime, timezone

coord1 = (-25, 152.4)
coord2 = (-25.2, 152.7)

#only use for pure data extraction, not the running of the CA
xsize = 750
ysize = 750

datesin = ['2019-11-12', '2019-11-13', '2019-11-14', '2019-11-15', '2019-11-16']
times = ['00:00', '12:00']

saveloc = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Outputs\Tests\Slope+Wind'

#FileLocations
waterfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Surface Water\EU Database\150E-20S'
waterfile = 'seasonality_150E_20S_v1_1.tif'

elefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\Australia'
elefile = '30S150E_20101117_gmted_mea075.tif'

firefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\FireData\Aus\Australia\DL_FIRE_V1_98928'
firefile = 'fire_nrt_V1_98928.shp'

weatherfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\GRIB\20-11 Aus'
weatherfile = 'adaptor.mars.internal-1595605290.199956-21027-5-86639461-543b-414f-b0ee-ae8c3230580b.grib'

roadfolder = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Road Data\Australia\australia-latest-free.shp"
roadfile = "gis_osm_roads_free_1.shp"

#Weather Data
hrspace = 12
startcoords = (-11, 130)

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

#Height Difference
delh = 50
