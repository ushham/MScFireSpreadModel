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

class RunData:

    def __init__(self):
        self.coord = (p.coord1, p.coord2)
        self.saveloc = p.saveloc
        self.elesave = "ElevationData"
        self.watsave =  self.saveloc + "\\" + "WaterData"
        self.barriersave = self.saveloc + "\\" + "FireBreaks"
        self.rows = d.n
        self.cols = d.m
        ##### Resolutions in km #####
        self.xres, self.yres = llt.Coord2Dist((self.coord[1][1] - self.coord[0][1]) / self.rows, (self.coord[1][0] - self.coord[0][0]) / self.cols, self.coord[0][1])

    def SlopeData(self):
        ######    Slope Data    ##########
        eleloc = p.elefolder + '\\' + p.elefile
        if d.ele:
            print('Extracting Elevation Data')

            delh = ed.Elevation(eleloc, self.coord[0], self.coord[1], self.rows, self.cols, self.saveloc, self.elesave).Extract_Data()
        else:
            arr = rc.readrst(self.saveloc + "\\" + self.elesave)
            delh = np.max(arr) - np.min(arr)
        return delh

    def WeatherData(self, delh):
        ######    Modified wind data #########
        if d.wth:
            wethloc = p.weatherfolder + '\\' + p.weatherfile

            reppday = 1
            dim = len(p.datesin) * len(p.times)
            uwind = np.empty((dim, self.cols, self.rows))
            vwind = np.empty((dim, self.cols, self.rows))
            i = 0


            print('Extracting Wind Data')
            for date in p.datesin:
                for time in p.times:
                    tim = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
                    sol = Wind_Data.WindData(wethloc, self.saveloc, tim, p.startcoords, self.coord[0], self.coord[1], self.rows, self.cols, False).Extract_Data()

                    uwind[i, :, :] = sol[0]
                    vwind[i, :, :] = sol[1]
                    i += 1

            #wind slope interaction
            xslope = np.genfromtxt(p.saveloc + "\\" + "xslope.csv", delimiter=",")
            yslope = np.genfromtxt(p.saveloc + "\\" + "yslope.csv", delimiter=",")

            print("Modifying Wind Data")
            for ell in range(dim):
                uwind[ell, :, :] = Wind_Slope.WindTopography(xslope, uwind[ell, :, :], delh, 1000 * self.xres, True).Data_Extract()
                vwind[ell, :, :] = Wind_Slope.WindTopography(yslope, vwind[ell, :, :], delh, 1000 * self.yres, False).Data_Extract()

                windloc = p.saveloc + "\\" + "WindData" + str(ell)
                rc.Convert2tif(uwind[ell, :, :], windloc + "-u", self.coord[0], self.coord[1], self.rows, self.cols, False)
                rc.Convert2tif(vwind[ell, :, :], windloc + "-v", self.coord[0], self.coord[1], self.rows, self.cols, False)

            return 0


    ######   Fire breaks   ########
    #Surface Water
    def SurfaceWater(self):
        if d.wat:
            print('Extracting Water Data')
            watloc = p.waterfolder + '\\' + p.waterfile
            water = WaterData.SurfaceWater(watloc, self.coord[0], self.coord[1], self.rows, self.cols, '').Extract_Data()
            rc.Convert2tif(water, watloc, self.coord[0], self.coord[1], self.rows, self.cols, False)
        else:
            water = 0
        return water

    #Road data
    def RoadData(self):
        if d.rod:
            print('Extracting Road Data')
            roadloc = p.roadfolder + "\\" + p.roadfile
            #make raster
            roadcl = rd.RoadData(roadloc, self.coord[0], self.coord[1], self.saveloc, self.rows, self.cols)
            roads = roadcl.roadrst(roadcl.shp2rst())
        else:
            roads = 0
        return roads

    #Combine Breaks
    def CombineBreaks(self):
        water = self.SurfaceWater()
        roads = self.RoadData()
        if d.rod and d.wat:

            breaks = np.multiply(water, roads)
        elif d.rod or d.wat:
            breaks = water if d.wat else roads
        else:
            breaks = 0

            #write tif of barriers
        if d.rod or d.wat:
            rc.Convert2tif(breaks, self.barriersave, self.coord[0], self.coord[1], self.rows, self.cols, False)
        return 0

    def ExtractAll(self):
        dh = self.SlopeData()
        self.WeatherData(dh)
        self.CombineBreaks()
        return 0







