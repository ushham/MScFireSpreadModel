import rasterio as rs
import pandas as pd
import numpy as np
from Mapping_Tools import LatLongTools as llt
from Mapping_Tools import RasterConvert as rc

#Exports the surface water in a given square to a given resolution
def Surface_Water(loc, coord1, coord2, xsize, ysize, dumploc):

    #constants
    seasonal = 1    #number of months/year water is present

    #x and y delta as angles
    delx = abs(coord1[0]-coord2[0]) / xsize
    dely = abs(coord1[1]-coord2[1]) / ysize

    #distance of each box in KM
    xdelta, ydelta = llt.Coord2Dist(delx, dely, coord1[0])

    #size of boxes in m
    print(str(xdelta * 1000) + 'm - xbox')
    print(str(ydelta * 1000) + 'm - ybox')

    #make matrix of coords
    elemat = np.zeros((ysize, xsize))

    #Coordinate Locations functions
    def xCoord(i):
        return coord1[1] + i * abs(coord1[1] - coord2[1]) / xsize
    def yCoord(i):
        return coord1[0] - i * abs(coord1[0] - coord2[0]) / ysize

    eledata = rs.open(loc)

    #Search each box location for water
    for i in range(ysize):
        for j in range(xsize):
            coord = (xCoord(j), yCoord(i))
            for val in eledata.sample([coord]):
                if val[0] > seasonal:
                    #if there is water we remove it
                    elemat[i, j] = 0
                else:
                    elemat[i, j] = 1

    savespot = dumploc + '\\' + 'WaterData'
    #Produce raster or return array
    if dumploc != '':
        rc.Convert2tif(elemat, savespot, coord1, coord2, xsize, ysize, False)
    else:
        return elemat

    return 0
