import rasterio as rs
import numpy as np
from Mapping_Tools import LatLongTools as llt
from Mapping_Tools import RasterConvert as rc
from scipy.interpolate import RegularGridInterpolator as rgi

class Elevation:
    def __init__(self, loc, coord1, coord2, xsize, ysize, dumploc, savename):
        self.fileloc = loc
        self.top_left = coord1
        self.bot_right = coord2
        self.xres = xsize
        self.yres = ysize
        self.saveloc = dumploc
        self.savename = savename
        self.save = self.saveloc + "\\" + self.savename

    def InturpEle(self, matrix):
        #interpolates initial elevation data to be of given size
        datasize = matrix.shape
        yres = (datasize[0] - 1) / self.yres
        xres = (datasize[1] - 1) / self.xres
        x, y = np.linspace(0, datasize[1] - 1, datasize[1]), np.linspace(0, datasize[0] - 1, datasize[0])
        grid = rgi((y, x), matrix)

        output = np.empty((self.yres, self.xres))
        for i in range(self.yres):
            yloc = i * yres
            for j in range(self.xres):
                xloc = j * xres
                output[i, j] = grid([yloc, xloc])

        return output

    def Elevation(self):
        print('Calculating Elevations')
        #coordinates
        left = self.top_left[1]
        right = self.bot_right[1]
        top = self.top_left[0]
        bott = self.bot_right[0]

        eledata = rs.open(self.fileloc)

        #index of coordinates
        row1, col1 = eledata.index(left, top)
        row2, col2 = eledata.index(right, bott)
        elearray = eledata.read(1)

        # make matrix of coords
        elemat = elearray[row1:(row2 + 1), col1:(col2 + 1)]

        output = self.InturpEle(elemat)
        delh = np.max(output) - np.min(output)

        # Output Elevation as Raster
        print('Saving Elevations')
        rc.Convert2tif(output, self.save, self.top_left, self.bot_right, self.xres, self.yres, False)
        #Output elevation results
        np.savetxt(self.save + '.csv', output, delimiter=',')
        return output, delh

    def Extract_Data(self):
        #Returns x and y directional slopes and elevations at given resolution
        #constants
        km2m = 1000
        quaddim = 3

        #find elevations and box size
        elemat, delh = self.Elevation()
        # x and y delta as angles
        delx = abs(self.top_left[0] - self.bot_right[0]) / self.xres
        dely = abs(self.top_left[1] - self.bot_right[1]) / self.yres

        # distance of each box in KM
        xdelta, ydelta = llt.Coord2Dist(delx, dely, self.top_left[0])
        xdelta = km2m * xdelta
        ydelta = km2m * ydelta

        xslope = np.zeros((self.yres, self.xres))
        yslope = np.zeros((self.yres, self.xres))

        #Approximate slope using 1st order method at boundaries, 2nd order in interior
        for i in range(self.xres):
            for j in range(self.yres):
                ########### X SLOPE #######
                if (i == 0):
                    xslope[j, i] = (elemat[j, i + 1] - elemat[j, i]) / xdelta
                elif (i == self.xres - 1):
                    xslope[j, i] = (elemat[j, i] - elemat[j, i - 1]) / xdelta
                else:
                    slopmat = np.zeros((quaddim, quaddim))
                    sol = np.array([elemat[j][i - 1], elemat[j][i], elemat[j][i + 1]])
                    for k in range(quaddim):
                        slopmat[k, :] = [(k * xdelta) ** 2, (k * xdelta), 1]

                    abc = np.array(np.linalg.solve(slopmat, sol))
                    #first derivative of resulting quadratic
                    xslope[j, i] = (2 * abc[0] + abc[1])

                #---Y slope---
                if (j == 0):
                    yslope[j, i] = (elemat[j + 1, i] - elemat[j, i]) / ydelta
                elif (j == self.yres - 1):
                    yslope[j, i] = (elemat[j, i] - elemat[j - 1, i]) / ydelta
                else:
                    slopmat = np.zeros((quaddim, quaddim))
                    sol = np.array([elemat[j - 1][i], elemat[j][i], elemat[j + 1][i]])
                    for k in range(3):
                        slopmat[k, :] = [(k * ydelta) ** 2, (k * ydelta), 1]

                    abc = np.array(np.linalg.solve(slopmat, sol))
                    yslope[j, i] = (2 * abc[0] + abc[1])


        savespotx = self.saveloc + '\\xslope.csv'
        savespoty = self.saveloc + '\\yslope.csv'
        np.savetxt(savespotx, xslope, delimiter=',')
        np.savetxt(savespoty, yslope, delimiter=',')
        return delh


