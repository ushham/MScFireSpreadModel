import numpy as np
import geopandas as gpd
from datetime import datetime
from datetime import time
from scipy.interpolate import griddata
from Mapping_Tools import RasterConvert as rc

class FireLayers:
    #Creates intopolated surfaces to display fire location from discrete observational data
    def __init__(self, loc, coord1, coord2, dumploc, hrspace, datesin, xsize, ysize):
        self.day2hour = 24
        self.firetime = 'ACQ_TIME'
        self.firedate = 'ACQ_DATE'
        self.firelat = 'LATITUDE'
        self.firelong = 'LONGITUDE'
        self.save = 'FireData'

        self.fileloc = loc
        self.top_left = coord1
        self.bot_right = coord2
        self.saveloc = dumploc
        self.date = datesin
        self.xres = xsize
        self.yres = ysize
        self.interval = hrspace

    def HourInt(self):
        #Returns array of times, given the hourly interval
        intervals = min(self.day2hour, self.interval)    #max hourly gap is 1 day

        numit = int(self.day2hour / intervals)
        timeint = []
        for i in range(numit):
            timeint.append(time(hour = int(i * self.day2hour / numit), minute = 0))

        timeint.append(time(hour = 23, minute = 59))    #end of day is added
        return timeint

    def FireLayerExtract(self, dateit, time):
        # Returns file of fire records within given area, on date within time band
        # Data Input file location
        firedf = gpd.read_file(self.fileloc)

        # calculates fire times
        timemin = time[0]
        timemax = time[1]

        # filters dataframe for only fires within the location box
        firedf = firedf[(firedf[self.firelat] < self.top_left[0]) & (firedf[self.firelat] > self.bot_right[0])]
        firedf = firedf[(firedf[self.firelong] > self.top_left[1]) & (firedf[self.firelong] < self.bot_right[1])]

        firedf[self.firetime] = firedf[self.firetime].apply(lambda x: datetime.strptime(x, '%H%M')).dt.time
        dttemp = firedf[(firedf[self.firedate] == dateit)]
        dttimetemp = dttemp[(dttemp[self.firetime] >= timemin) & (dttemp[self.firetime] <= timemax)]

        if dttimetemp.shape[0] > 0:
            dttimetemp = dttimetemp.drop([self.firetime], axis=1)
            out = dttimetemp
            run = True
        else:
            out = 0
            run = False

        return run, out

    def CreateSurface(self, firedata, saveloc):
        # Opens file, or expected df to be passed, and returns a sursafe of expected fire based on FRP
        # Saves a raster of surface
        # constants
        lat = 'LATITUDE'
        long = 'LONGITUDE'
        conf = 'FRP'
        min_points = 4

        # set size of arrays
        points = np.array(firedata[[lat, long]])
        delx = abs(self.top_left[1] - self.bot_right[1]) / self.xres
        dely = abs(self.top_left[0] - self.bot_right[0]) / self.yres

        # create evenly spaced array given number of boxes
        x = np.arange(min(self.top_left[1], self.bot_right[1]), max(self.top_left[1], self.bot_right[1]), delx)
        y = np.arange(max(self.top_left[0], self.bot_right[0]), min(self.top_left[0], self.bot_right[0]), -dely)

        grid_x, grid_y = np.meshgrid(x, y)

        pointy = points[:, 0]
        pointx = points[:, 1]

        # create surface
        # Check if there are enough points to make surface
        if len(firedata.index) >= min_points:
            z = griddata((pointx, pointy), firedata[conf], (grid_x, grid_y), method='linear')
            # Convert surface to raster file
            rc.Convert2tif(z, saveloc, self.top_left, self.bot_right, self.xres, self.yres, False)
        else:
            print('Not enough points at ' + self.saveloc)
        return 0

    def Extract_Data(self):
        time = self.HourInt()
        for i in self.date:
            for j in range(len(time) - 1):
                timeint = [time[j], time[j+1]]
                run, firedat = self.FireLayerExtract(i, timeint)
                if run:
                    dumploc = self.saveloc + '\\' + str(i) + '-' + str(time[j])[0:2]
                    print(dumploc)
                    self.CreateSurface(firedat, dumploc)
        return 0