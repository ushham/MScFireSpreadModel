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
ed.ElevationSlope(eleloc, coord1, coord2, xsize, ysize, saveloc, 'ElevationData')

#Extract Surface Water Data
print('Extracting Surface Water Data')
watloc = p.waterfolder + '\\' + p.waterfile
wd.Surface_Water(watloc, coord1, coord2, xsize, ysize, saveloc)

#Extract Fire Data
print('Extracting Fire Data')
fireloc = p.firefolder + '\\' + p.firefile
fd.IterateFire(fireloc, saveloc + '\\FireData', p.hrspace, datesin, coord1, coord2, xsize, ysize)

#Extract Wind Data
print('Extracting Wind Data')
wethloc = p.weatherfolder + '\\' + p.weatherfile

reppday = 1
wnd.WindDat(wethloc, saveloc, p.dt, len(datesin), p.hrspace / reppday, p.startcoords, coord1, coord2, xsize, ysize)
