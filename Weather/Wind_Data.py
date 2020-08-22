from datetime import timedelta
from Weather import Grib_Ext as ge
import numpy as np
from Mapping_Tools import RasterConvert as rc

class WindData:
    def __init__(self, fileloc, dumploc, dt, coordstart, coord1, coord2, xres, yres, save):
        self.fileloc = fileloc
        self.saveloc = dumploc
        self.time = dt
        self.coord0 = coordstart
        self.top_left = coord1
        self.bot_right = coord2
        self.xres = xres
        self.yres = yres
        self.res = 0.25
        self.save = save

    # calculate number of grib coords to extract
    def delx(self):
        return int((abs(round(self.top_left[1] * 1 / self.res) / (1 / self.res) - round(self.bot_right[1] * 1 / self.res) / (1 / self.res))) / self.res) + 1

    def dely(self):
        return int((abs(round(self.top_left[0] * 1 / self.res) / (1 / self.res) - round(self.bot_right[0] * 1 / self.res) / (1 / self.res))) / self.res) + 1

    #reads in dates and times and produces wind array of area
    def Extract_Data(self):
        dx = self.delx()
        dy = self.dely()

        #Extract 10m u and v components of wind from GRIB
        print('Extracting GRIB')
        u = ge.GribExtract(self.fileloc, self.coord0, self.top_left, self.time, '10U', dx, dy)
        v = ge.GribExtract(self.fileloc, self.coord0, self.top_left, self.time, '10V', dx, dy)

        u = u.Extract_Data()
        v = v.Extract_Data()

        ######convert small array to big array######
        uout = np.zeros((self.yres, self.xres))
        vout = np.zeros((self.yres, self.xres))

        print('Reshaping GRIB')
        for x in range(self.xres):
            #round to nearest grid
            xloc = self.top_left[1] + x * abs(self.top_left[1] - self.bot_right[1]) / self.xres
            xloc = round(xloc * 1 / self.res) / (1 / self.res)
            for y in range(self.yres):
                yloc = self.top_left[0] + y * abs(self.top_left[0] - self.bot_right[0]) / self.yres
                yloc = round(yloc * 1 / self.res) / (1 / self.res)

                x1 = int(abs(xloc - self.top_left[1]) / self.res)
                y1 = int(abs(yloc - self.top_left[0]) / self.res)

                uout[y, x] = u[y1, x1]
                vout[y, x] = v[y1, x1]

        #print out array
        hourout = str(self.time.hour)
        dayout = str(self.time.day)

        if self.save:
            saveloc = self.fileloc + '\\' + dayout + '-' + hourout
            ######Convert to tif files
            rc.Convert2tif(uout, saveloc + 'u', self.top_left, self.bot_right, dx, dy, False)
            rc.Convert2tif(vout, saveloc + 'v', self.top_left, self.bot_right, dx, dy, False)
        else:

            return uout, vout
        return 0
