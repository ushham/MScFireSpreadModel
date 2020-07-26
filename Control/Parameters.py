from datetime import datetime, timezone

coord1 = (-11.657, 130.83)
coord2 = (-11.92, 131.138)

xsize = 400
ysize = 400

datesin = ['2019-10-01', '2019-10-02', '2019-10-03', '2019-10-04', '2019-10-05', '2019-10-06', '2019-10-07', '2019-10-08', '2019-10-09']

saveloc = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Outputs\Tiwi Isl'

#FileLocations
waterfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Surface Water\EU Database\150E-20S'
waterfile = 'seasonality_150E_20S_v1_1.tif'

elefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\Australia'
elefile = '30S120E_20101117_gmted_mea075.tif'

firefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\FireData\Aus\Australia\DL_FIRE_V1_98928'
firefile = 'fire_nrt_V1_98928.shp'

weatherfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\GRIB\20-10 Aus'
weatherfile = 'adaptor.mars.internal-1595755000.980882-25690-1-11fe5f5b-ea86-4ebf-859b-b216d85f2cdd.grib'

#Fire Data
hrspace = 12
dt = datetime(2019, 10, 1, 0, 0, 0, 0, timezone.utc)
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