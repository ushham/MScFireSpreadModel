from osgeo import gdal
from datetime import datetime
import numpy as np

#GRIB Constants
#resolution of GRIB files in degrees

class GribExtract:
    def  __init__(self, fileloc, coordstart, coord1, datet, ele, nx, ny):
        self.res = 0.25
        self.fileloc = fileloc
        self.coord0 = coordstart
        self.top_left = coord1
        self.time = datet
        self.mat = ele
        self.xres = nx
        self.yres = ny

        #Data Labels
        self.timelabel = 'GRIB_REF_TIME'
        self.elementlabel = 'GRIB_ELEMENT'

    def CoordX(self, x):
        coordx = round(((self.top_left[1] - self.coord0[1]) + self.res * x) * (1 / self.res)) / (1 / self.res)
        coordx = int(coordx / self.res)
        return coordx


    def CoordY(self, y):
        coordy = round(((self.coord0[0] - self.top_left[0]) - self.res * y) * (1 / self.res)) / (1 / self.res)
        coordy = int(coordy / self.res)
        return coordy


    def Extract_Data(self):
        #Open file
        dataset = gdal.Open(self.fileloc, gdal.GA_ReadOnly)
        message_count = dataset.RasterCount
        unixtime = datetime.timestamp(self.time)

        out = None
        for i in range(1, message_count):
            #Extract data from GRIB
            message = dataset.GetRasterBand(i).GetMetadata()
            #extract time
            timeband = message[self.timelabel]
            timeband = timeband.split()
            #extract element label
            type = message[self.elementlabel]

            if int(timeband[0]) == unixtime and type == self.mat:
                out = np.zeros((self.xres, self.yres))
                for x in range(self.xres):
                    for y in range(self.yres):
                        out[x, y] = dataset.GetRasterBand(i).ReadAsArray()[self.CoordY(y), self.CoordX(x)]

        return out


