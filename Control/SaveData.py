from Elevations import ElevationData as ed
from Surface_Water import WaterData as wd
from Fire_Locations import FireData as fd
from Mapping_Tools import LatLongTools as llt
from Control import Parameters as p
from Weather import Wind_Data as wnd

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
eleloc = p.elefolder + '\\' + p.elefile
elevation = ed.Elevation(eleloc, coord1, coord2, xsize, ysize, saveloc, 'ElevationData')

#Extract Surface Water Data
print('Extracting Surface Water Data')
watloc = p.waterfolder + '\\' + p.waterfile
water = wd.SurfaceWater(watloc, coord1, coord2, xsize, ysize, saveloc)

#Extract Fire Data
print('Extracting Fire Data')
fireloc = p.firefolder + '\\' + p.firefile
fire = fd.FireLayers(fireloc, coord1, coord2, saveloc, p.hrspace, datesin, xsize, ysize)
f = fire.Extract_Data()

#Extract Wind Data
print('Extracting Wind Data')
wethloc = p.weatherfolder + '\\' + p.weatherfile

reppday = 1
wind = wnd.WindData(wethloc, saveloc, p.datesin, p.startcoords, coord1, coord2, xsize, ysize)
win = wind.Extract_Data()