import rasterio as rs
import numpy as np
from Mapping_Tools import LatLongTools as llt
from Mapping_Tools import RasterConvert as rc
from scipy.interpolate import RegularGridInterpolator as rgi

def InturpEle(data, xsiz, ysiz):
    #interpolates initial elevation data to be of given size
    datasize = data.shape
    yres = (datasize[0] - 1) / ysiz
    xres = (datasize[1] - 1) / xsiz
    x, y = np.linspace(0, datasize[1] - 1, datasize[1]), np.linspace(0, datasize[0] - 1, datasize[0])
    grid = rgi((y, x), data)

    output = np.empty((ysiz, xsiz))
    for i in range(ysiz):
        yloc = i * yres
        for j in range(xsiz):
            xloc = j * xres
            output[i, j] = grid([yloc, xloc])

    return output

def Elevation(loc, coord1, coord2, xsize, ysize, dumploc, savename):
    #coordinates
    left = coord1[1]
    right = coord2[1]
    top = coord1[0]
    bott = coord2[0]

    eledata = rs.open(loc)

    #index of coordinates
    row1, col1 = eledata.index(left, top)
    row2, col2 = eledata.index(right, bott)
    elearray = eledata.read(1)

    # make matrix of coords
    elemat = elearray[row1:(row2 + 1), col1:(col2 + 1)]

    output = InturpEle(elemat, xsize, ysize)
    delh = np.max(output) - np.min(output)

    savespot = dumploc + '\\' + savename
    # Output Elevation as Raster

    rc.Convert2tif(output, savespot, coord1, coord2, xsize, ysize, False)
    #Output elevation results
    np.savetxt(savespot + 'csv', output, delimiter=',')
    return output, delh



def ElevationSlope(loc, coord1, coord2, xsize, ysize, dumploc, savename):
    #Returns x and y directional slopes and elevations at given resolution
    #constants
    km2m = 1000
    quaddim = 3

    #find elevations and box size
    elemat, delh = Elevation(loc, coord1, coord2, xsize, ysize, dumploc, savename)
    # x and y delta as angles
    delx = abs(coord1[0] - coord2[0]) / xsize
    dely = abs(coord1[1] - coord2[1]) / ysize

    # distance of each box in KM
    xdelta, ydelta = llt.Coord2Dist(delx, dely, coord1[0])
    xdelta = km2m * xdelta
    ydelta = km2m * ydelta
    print(xdelta, ydelta)

    xslope = np.zeros((ysize, xsize))
    yslope = np.zeros((ysize, xsize))

    #Approximate slope using 1st order method at boundaries, 2nd order in interior
    for i in range(xsize):
        for j in range(ysize):
            ########### X SLOPE #######
            if (i == 0):
                xslope[j, i] = (elemat[j, i + 1] - elemat[j, i]) / xdelta
            elif (i == xsize - 1):
                xslope[j, i] = (elemat[j, i] - elemat[j, i - 1]) / xdelta
            else:
                slopmat = np.zeros((quaddim, quaddim))
                sol = np.array([elemat[j][i - 1], elemat[j][i], elemat[j][i + 1]])
                for k in range(quaddim):
                    slopmat[k, 0] = (k * xdelta) ** 2
                    slopmat[k, 1] = (k * xdelta)
                    slopmat[k, 2] = 1

                abc = np.array(np.linalg.solve(slopmat, sol))
                #first derivative of resulting quadratic
                xslope[j, i] = (2 * abc[0] + abc[1])

            #---Y slope---
            if (j == 0):
                yslope[j, i] = (elemat[j + 1, i] - elemat[j, i]) / ydelta
            elif (j == ysize - 1):
                yslope[j, i] = (elemat[j, i] - elemat[j - 1, i]) / ydelta
            else:
                slopmat = np.zeros((quaddim, quaddim))
                sol = np.array([elemat[j - 1][i], elemat[j][i], elemat[j + 1][i]])
                for k in range(3):
                    slopmat[k, 0] = (k * ydelta) ** 2
                    slopmat[k, 1] = (k * ydelta)
                    slopmat[k, 2] = 1

                abc = np.array(np.linalg.solve(slopmat, sol))
                yslope[j, i] = (2 * abc[0] + abc[1])


    savespotx = dumploc + '\\xslope.csv'
    savespoty = dumploc + '\\yslope.csv'
    np.savetxt(savespotx, xslope, delimiter=',')
    np.savetxt(savespoty, yslope, delimiter=',')
    return delh



coord2 = (39.651237, -121.403610)
coord1 = (39.737094, -121.543857)
loc = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\US\GMTED2010 Data\FID25-NW USA\30N150W_20101117_gmted_mea075.tif"
fold = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\US\GMTED2010 Data\FID25-NW USA"
ElevationSlope(loc, coord1, coord2, 100, 100, fold, "poetest")