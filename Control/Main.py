from Elevations import ElevationData as ed
from Surface_Water import WaterData as wd
from Fire_Locations import FireData as fd
from Mapping_Tools import LatLongTools as llt
from Control import Parameters as p
from Weather import Wind_Data as wnd
from datetime import datetime

#Data sources
waterfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Surface Water\EU Database\150E-20S'
waterfile = 'seasonality_150E_20S_v1_1.tif'

elefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\Australia'
elefile = '30S120E_20101117_gmted_mea075.tif'

firefolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\FireData\Aus\Aus 20191123 VIIRS'
firefile = 'fire_nrt_V1_88533.shp'

weatherfolder = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\GRIB\North WA'
weatherfile = 'adaptor.mars.internal-1595493664.1122472-2895-20-c95be05b-c013-41fc-8dc4-dde31d62b056.grib'

saveloc = p.saveloc

xsize = p.xsize
ysize = p.ysize

coord1 = p.coord1
coord2 = p.coord2

datesin = p.datesin

#Print lat and long data
llt.PrintLatLong(saveloc, coord1, coord2, xsize, ysize)

#Extract Elevation Data
print('Extracting Elevation Data')
eleloc = elefolder + '\\' + elefile
#ed.ElevationSlope(eleloc, coord1, coord2, xsize, ysize, saveloc, 'ElevationData')

#Extract Surface Water Data
print('Extracting Surface Water Data')
watloc = waterfolder + '\\' + waterfile
#wd.Surface_Water(watloc, coord1, coord2, xsize, ysize, saveloc, 'WaterData')

#Extract Fire Data
print('Extracting Fire Data')
fireloc = firefolder + '\\' + firefile
fd.IterateFire(fireloc, saveloc + '\\FireData', p.hrspace, datesin, coord1, coord2, xsize, ysize)

#Extract Wind Data
print('Extracting Wind Data')
wethloc = weatherfolder + '\\' + weatherfile
dt = datetime(2019, 11, 16, 0, 0)
reppday = 1
wnd.WindDat(wethloc, saveloc, dt, len(datesin), p.hrspace / reppday, (-11, 130), coord1, coord2, xsize, ysize)

#Produce Wind/Slope