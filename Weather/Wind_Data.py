from datetime import timedelta
from Weather import Grib_Ext as ge
import numpy as np
from Mapping_Tools import RasterConvert as rc

#reads in dates and times and produces wind array of area
def WindDat(fileloc, dumploc, datestart, days, hourgap, coordstart, coord1, coord2, xres, yres):
    resolution = ge.res
    near = 1 / resolution

    #calculate number of grib coords to extract
    delx = int((abs(round(coord1[1] * near) / near - round(coord2[1] * near) / near)) / resolution) + 1
    dely = int((abs(round(coord1[0] * near) / near - round(coord2[0] * near) / near)) / resolution) + 1


    #calc number of time steps
    day2hour = 24
    delh = int(day2hour / hourgap)

    timeits = days * delh

    for time in range(timeits):
        tim = datestart + timedelta(hours = hourgap * time)

        u = ge.GribExt(fileloc, coordstart, coord1, tim, '10U', delx, dely)
        v = ge.GribExt(fileloc, coordstart, coord1, tim, '10V', delx, dely)

        #convert small array to big array
        uout = np.zeros((xres, yres))
        vout = np.zeros((xres, yres))

        for x in range(xres):
            #round to nearest grid
            xloc = coord1[1] + x * abs(coord1[1] - coord2[1]) / xres
            xloc = round(xloc * near) / near
            for y in range(yres):
                yloc = coord1[0] + y * abs(coord1[0] - coord2[0]) / xres
                yloc = round(yloc * near) / near

                x1 = int(abs(xloc - coord1[1]) / resolution)
                y1 = int(abs(yloc - coord1[0]) / resolution)

                uout[x, y] = u[x1, y1]
                vout[x, y] = v[x1, y1]

        #print out array
        hourout = str(tim.hour)
        dayout = str(tim.day)

        saveloc = dumploc + '\\' + dayout + '-' + hourout
        #np.savetxt(saveloc + 'u.csv', uout, delimiter=',')
        #np.savetxt(saveloc + 'v.csv', vout, delimiter=',')
        rc.Convert2tif(uout, saveloc + 'u', coord1, coord2, xres, yres, False)
        rc.Convert2tif(vout, saveloc + 'v', coord1, coord2, xres, yres, False)
    return 0