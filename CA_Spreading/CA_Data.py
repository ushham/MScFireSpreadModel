from CA_Spreading import CA_Definition as d
from Control import Parameters as p
from Weather import Wind_Data, Wind_Slope
from Elevations import ElevationData as ed
from Surface_Water import WaterData
from datetime import datetime
from Barriers import RoadData as rd
from Mapping_Tools import RasterConvert as rc
from Mapping_Tools import LatLongTools as llt
import numpy as np

#Save names
elesav = "ElevationData"
watsav = p.saveloc + "\\" + "WaterData"
barriersav = p.saveloc + "\\" + "FireBreaks"
anisav = p.saveloc + "\\" + "animationALLTEST"

coord = (p.coord1, p.coord2)

def RunData():
    ##### Resolutions in km #####
    xres, yres = llt.Coord2Dist((coord[1][1] - coord[0][1]) / d.n, (coord[1][0] - coord[0][0]) / d.m, coord[0][1])

    ######    Slope Data    ##########
    eleloc = p.elefolder + '\\' + p.elefile
    if d.ele:
        print('Extracting Elevation Data')
        delh = ed.ElevationSlope(eleloc, coord[0], coord[1], d.n, d.m, p.saveloc, elesav)


    ######    Modified wind data #########
    wethloc = p.weatherfolder + '\\' + p.weatherfile

    reppday = 1
    dim = len(p.datesin) * len(p.times)
    uwind = np.empty((dim, d.m, d.n))
    vwind = np.empty((dim, d.m, d.n))
    i = 0
    if d.wth:
        if not(d.ele):
            delh = p.delh

        print('Extracting Wind Data')
        for date in p.datesin:
            for time in p.times:
                tim = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
                print(tim)

                res = Wind_Data.WindDat(wethloc, p.saveloc, tim, p.startcoords, coord[0], coord[1], d.n, d.m, False)

                uwind[i, :, :] = res[0]
                vwind[i, :, :] = res[1]
                i += 1

        #wind slope interaction
        xslope = np.genfromtxt(p.saveloc + "\\" + "xslope.csv", delimiter=",")
        yslope = np.genfromtxt(p.saveloc + "\\" + "yslope.csv", delimiter=",")

        for ell in range(dim):
            uwind[ell, :, :] = Wind_Slope.SlopeWind(xslope, uwind[ell, :, :], delh, 1000 * xres, True)
            vwind[ell, :, :] = Wind_Slope.SlopeWind(yslope, vwind[ell, :, :], delh, 1000 * yres, False)

            windloc = p.saveloc + "\\" + "WindData" + str(ell)
            rc.Convert2tif(uwind[ell, :, :], windloc + "-u", coord[0], coord[1], d.n, d.m, False)
            rc.Convert2tif(vwind[ell, :, :], windloc + "-v", coord[0], coord[1], d.n, d.m, False)


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
    elif d.rod or d.wat:
        breaks = water if d.wat else roads

        #write tif of barriers
    if d.rod or d.wat:
        rc.Convert2tif(breaks, barriersav, coord[0], coord[1], d.n, d.m, False)

    return 0





