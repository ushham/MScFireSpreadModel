from datetime import datetime, timezone

coord1 = (-35.53, 136.52)
coord2 = (-36.09, 138.2)

#only use for pure data extraction, not the running of the CA
xsize = 750
ysize = 750

datesin = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05']
times = ['00:00', '12:00']

saveloc = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Outputs\01 Results\Kangaroo Island\Runs'

#FileLocations
waterfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Surface Water\EU Database\150E-20S'
waterfile = 'seasonality_130E_30Sv1_1_2019.tif'

elefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\Australia'
elefile = '50S120E_20101117_gmted_mea075.tif'

firefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\FireData\Aus\Australia\DL_FIRE_V1_98928'
firefile = 'fire_nrt_V1_98928.shp'

weatherfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\GRIB\Aus 20-01'
weatherfile = 'adaptor.mars.internal-1598775148.4113145-23698-28-20b6975b-f5a7-4021-9fcc-babe0006c5c4.grib'

roadfolder = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Road Data\Australia\australia-latest-free.shp"
roadfile = "gis_osm_roads_free_1.shp"

#Weather Data
hrspace = 12
startcoords = (-12, 111)

#Windspeed/hill length interaction
windfact = 0.1      #Parameter to allter effect of slope on wind speed
windhill = 8 / 5    #Calibrated Wind speed increase dependant on height
upperwindlim = 3    #Maximum windspeed increase from base

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
