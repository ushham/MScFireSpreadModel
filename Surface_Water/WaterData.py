import rasterio as rs
import numpy as np
from Mapping_Tools import LatLongTools as llt
from Mapping_Tools import RasterConvert as rc

class SurfaceWater:
    def __init__(self, loc, coord1, coord2, xsize, ysize, dumploc):
        self.loc = loc
        self.top_left = coord1
        self.bot_right = coord2
        self.xres = xsize
        self.yres = ysize
        self.saveloc = dumploc
        self.season = 1 #number of months/year water is present

    # Coordinate Locations functions
    def xCoord(self, i):
        return self.top_left[1] + i * abs(self.top_left[1] - self.bot_right[1]) / self.xres

    def yCoord(self, i):
        return self.top_left[0] - i * abs(self.top_left[0] - self.bot_right[0]) / self.yres

    #Exports the surface water in a given square to a given resolution
    def Extract_Data(self):
        #x and y delta as angles
        delx = abs(self.top_left[1] - self.bot_right[1]) / self.xres
        dely = abs(self.top_left[0] - self.bot_right[0]) / self.yres

        #distance of each box in KM
        xdelta, ydelta = llt.Coord2Dist(delx, dely, self.top_left[0])

        #size of boxes in m
        print(str(xdelta * 1000) + 'm - xbox')
        print(str(ydelta * 1000) + 'm - ybox')

        #make matrix of coords
        elemat = np.zeros((self.yres, self.xres))
        eledata = rs.open(self.loc)

        #Search each box location for water
        for i in range(self.yres):
            for j in range(self.xres):
                coord = (self.xCoord(j), self.yCoord(i))
                for val in eledata.sample([coord]):
                    if val[0] > self.season:
                        #if there is water we remove it
                        elemat[i, j] = 0
                    else:
                        elemat[i, j] = 1

        savespot = self.saveloc + '\\' + 'WaterData'
        #Produce raster or return array
        if self.saveloc != '':
            rc.Convert2tif(elemat, savespot, self.top_left, self.bot_right, self.xres, self.yres, False)
        else:
            return elemat

        return 0
