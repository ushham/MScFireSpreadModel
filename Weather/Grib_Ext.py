from osgeo import gdal
from datetime import datetime
import numpy as np

#GRIB Constants
#resolution of GRIB files in degrees
res = 0.25

#Data Labels
timelabel = 'GRIB_REF_TIME'
elementlabel = 'GRIB_ELEMENT'

def GribExt(fileloc, coordstart, datet, ele, nx, ny):
    #Open file
    resinv = 1 / res
    dataset = gdal.Open(fileloc, gdal.GA_ReadOnly)
    message_count = dataset.RasterCount

    unixtime = datetime.timestamp(datet)
    out = None
    for i in range(1, message_count):
        #Extract data from GRIB
        message = dataset.GetRasterBand(i).GetMetadata()
        #extract time
        timeband = message[timelabel]
        timeband = timeband.split()
        #extract element label
        type = message[elementlabel]

        if int(timeband[0]) == unixtime and type == ele:
            out = np.zeros((nx, ny))
            for x in range(nx):
                for y in range(ny):
                    coordy = round((coordstart[0] - res * y) * resinv) / resinv
                    coordx = round((coordstart[1] + res * x) * resinv) / resinv

                    coordx = int((coordx - coordstart[1]) / res)
                    coordy = int((coordstart[0] - coordy) / res)

                    out[x, y] = dataset.GetRasterBand(i).ReadAsArray()[coordx, coordy]

    return out


