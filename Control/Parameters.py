from datetime import datetime, timezone

coord1 = (39.922, -121.8)
coord2 = (39.6, -121.31)

#only use for pure data extraction, not the running of the CA
xsize = 750
ysize = 750

datesin = ['2018-11-08', '2018-11-09', '2018-11-10', '2018-11-11', '2018-11-12']
times = ['00:00', '12:00']

saveloc = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Outputs\01 Results\Camp Fire\Runs'

#FileLocations
waterfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Surface Water\EU Database\130W-40N'
waterfile = 'seasonality_130W_40N_v1_1.tif'

elefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\US\GMTED2010 Data\FID25-NW USA'
elefile = '30N150W_20101117_gmted_mea075.tif'

firefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\FireData\USA 2018\DL_FIRE_V1_149275'
firefile = 'fire_archive_V1_149275.shp'

weatherfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\GRIB\California'
weatherfile = 'adaptor.mars.internal-1598787975.3658226-7819-13-fb769ce2-840e-40d5-9f6b-2dec334a7040.grib'

roadfolder = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Road Data\California\norcal-latest-free"
roadfile = "gis_osm_roads_free_1.shp"

#Weather Data
hrspace = 12
startcoords = (42, -125)

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
