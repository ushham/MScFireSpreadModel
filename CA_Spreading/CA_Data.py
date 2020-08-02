from CA_Spreading import CA_Definition as d
from Control import Parameters as p
from Weather import Wind_Data, Wind_Slope
from Elevations import ElevationData as ed
from Surface_Water import WaterData
from datetime import datetime
from Barriers import RoadData as rd
from Mapping_Tools import RasterConvert as rc
import numpy as np

#Save names
elesav = "ElevationData"
watsav = p.saveloc + "\\" + "WaterData"
barriersav = p.saveloc + "\\" + "FireBreaks"
anisav = p.saveloc + "\\" + "animation"

coord = (p.coord1, p.coord2)
def RunData():
    ######    Slope Data    ##########
    eleloc = p.elefolder + '\\' + p.elefile
    if d.ele:
        print('Extracting Elevation Data')
        xslope, yslope, delh = ed.ElevationSlope(eleloc, coord[0], coord[1], d.n, d.m, '', elesav)


    ######    Modified wind data #########
    wethloc = p.weatherfolder + '\\' + p.weatherfile

    reppday = 1
    uwind = []
    vwind = []
    if d.wth:
        print('Extracting Wind Data')
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

    ######   Fire breaks   ########
    #Surface Water
    if d.wat:
        print('Extracting Water Data')
        watloc = p.waterfolder + '\\' + p.waterfile
        water = WaterData.Surface_Water(watloc, coord[0], coord[1], d.n, d.m, '')
        rc.Convert2tif(water, watloc, coord[0], coord[1], d.n, d.m, False)

    #Road data
    if d.rod:
        print('Extracting Road Data')
        roadloc = p.roadfolder + "\\" + p.roadfile
        #make raster
        roads = rd.roadrst(rd.shp2rst(roadloc, coord[0], coord[1], d.n, d.m, p.saveloc))

    #Combine Breaks
    if d.rod and d.wat:
        breaks = np.multiply(water, roads)

        #write tif of barriers
        rc.Convert2tif(breaks, barriersav, coord[0], coord[1], d.n, d.m, False)

    return 0








