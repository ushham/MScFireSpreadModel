from datetime import datetime, timezone

coord1 = (-25, 152.4)
coord2 = (-25.2, 152.7)

#only use for pure data extraction, not the running of the CA
xsize = 750
ysize = 750

datesin = ['2019-12-21', '2019-12-22', '2019-12-23', '2019-12-24', '2019-12-25', '2019-12-26', '2019-12-27']

saveloc = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Outputs\Tests'

#FileLocations
waterfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Surface Water\EU Database\150E-20S'
waterfile = 'seasonality_150E_20S_v1_1.tif'

elefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\Australia'
elefile = '50S120E_20101117_gmted_mea075.tif'

firefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\FireData\Aus\Australia\DL_FIRE_V1_98928'
firefile = 'fire_nrt_V1_98928.shp'

weatherfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\GRIB\20-12 Aus'
weatherfile = 'adaptor.mars.internal-1595771507.6347456-24243-13-98b6c595-d201-4bf7-91fd-1e9853c2c788.grib'

roadfolder = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Road Data\Australia\australia-latest-free.shp"
roadfile = "gis_osm_roads_free_1.shp"

#Fire Data
hrspace = 12
dt = datetime(2019, 12, 21, 0, 0, 0, 0, timezone.utc)
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