from CA_Spreading import CA_Definition as d
from Control import Parameters as p
from Weather import Wind_Data, Wind_Slope
from Elevations import ElevationData as ed
from Surface_Water import WaterData
from datetime import datetime
import numpy as np

coord = (p.coord1, p.coord2)

######    Slope Data    ##########
print('Extracting Elevation Data')
eleloc = p.elefolder + '\\' + p.elefile
xslope, yslope, delh = ed.ElevationSlope(eleloc, coord[0], coord[1], d.n, d.m, '', 'ElevationData')


######    Modified wind data #########
print('Extracting Wind Data')
wethloc = p.weatherfolder + '\\' + p.weatherfile

reppday = 1
uwind = []
vwind = []
for date in d.dates:
    for time in d.times:
        tim = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
        res = Wind_Data.WindDat(wethloc, '', p.dt, tim, p.startcoords, coord[0], coord[1], d.n, d.m)
        uwind.append(res[0])
        vwind.append(res[1])

#wind slope interaction
for i in range(min(uwind.shape[0], vwind.shape[0])):
    uwind[i, :, :] = Wind_Slope.SlopeWind(xslope, uwind[i, :, :], delh, True)
    vwind[i, :, :] = Wind_Slope.SlopeWind(yslope, vwind[i, :, :], delh, False)

######   Wind breaks   ########
#Surface Water
watloc = p.waterfolder + '\\' + p.waterfile
water = WaterData.Surface_Water(watloc, coord[0], coord[1], d.n, d.m, '')

#Road data


#Combine Breaks







