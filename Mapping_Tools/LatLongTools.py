import numpy as np
from Mapping_Tools import RasterConvert as rc

def CoordLoc(coord):
    #inputs coordinate, returns (n, e) = (true/false, true/false)
    #assume in lat, long format
    equator = 0
    meridian = 0
    dateline = 180
    poles = 90

    #Checks location is valid
    if abs(coord[0]) > poles or abs(coord[1]) > dateline:
        print('Coordinate ' + coord + ' is not valid')
        return 1
    n, e = 0, 0
    if coord[0] >= equator:
        n = 1
    if coord[1] > meridian:
        e = 1

    return [n, e]

def Coord2Dist(delx, dely, lat):
    #Returns distance given grid size
    erad = 6371  # radius of the earth in km
    deg = 360  # degress per 2 radians
    tau = 2 * np.pi

    xdelta = (delx / deg) * erad * tau
    ydelta = (dely / deg) * np.sin(tau / 4 - abs(lat) * tau / deg) * erad * tau
    return xdelta, ydelta

def PrintLatLong(dumploc, coord1, coord2, xres, yres):
    delx = abs(coord1[1] - coord2[1]) / xres
    dely = abs(coord1[0] - coord2[0]) / yres

    lat = np.empty((xres, yres))
    long = np.empty((xres, yres))

    for i in range(xres):
        for j in range(yres):
            lat[j, i] = coord1[0] - dely * j
            long[j, i] = coord1[1] + delx * i

    rc.Convert2tif(lat, dumploc + '\\' +'lat', coord1, coord2, xres, yres, False)
    rc.Convert2tif(long, dumploc + '\\' + 'lon', coord1, coord2, xres, yres, False)
    return 0