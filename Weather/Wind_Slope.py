import numpy as np
from Control import Parameters

funcdata = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\CSVs\Slope-Wind\Slope-Wind 200711.csv"
thetastore = np.genfromtxt(funcdata, delimiter=',')

def tau(theta, hf):
    #Function which returns increase in wind velocity due to slope
    #Assuming function is to 3 decimals of precision
    gap = thetastore[0, 1] - thetastore[0, 0]
    start = theta - thetastore[0, 0]
    loc = int(start / gap)
    return thetastore[1, loc] * hf + 1


def SlopeWind(slope, wind, delh, res, bool):
    lowerlim = 0    #Wind cannot be less than 0
    upperlim = Parameters.upperwindlim * wind   #% increase allowed
    #2d array of slope and 1 d array of wind at same resolution, true = u, false = v

    #delh - hill length - grid resolution:
    ell = delh * Parameters.windhill
    hillfact = res / ell

    outarr = np.zeros(slope.shape)
    if bool:
        #u direction (by column)
        if wind > 0: #Westerly wind (left to right)
            rng = range(0, slope.shape[1])
            side = - 1
        else:
            rng = range(slope.shape[1] - 1, -1, -1)
            side = 1
        for j in range(slope.shape[0]):
            for i in rng:
                if i == rng[0]:
                    outarr[j, i] = wind * tau(slope[j, i], hillfact)
                else:
                    outarr[j, i] = outarr[j, i + side] * tau(slope[j, i], hillfact)

    else:
        # v direction (by row)
        if wind < 0:  # Northly wind (top to bottom)
            rng = range(0, slope.shape[0])
            side = -1
        else:
            rng = range(slope.shape[0] - 1, -1, -1)
            side = 1
        for j in range(slope.shape[1]):
            for i in rng:
                if i == rng[0]:
                    outarr[i, j] = wind * tau(slope[j, i], hillfact)
                else:
                    outarr[i, j] = outarr[i + side, j] * tau(slope[i, j], hillfact)

    return outarr

fileloc = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Altitudes\US\GMTED2010 Data\FID25-NW USA\yslope.csv"
u = -1.3992767
v = -2.41806
inp = np.genfromtxt(fileloc, delimiter=',')
yres = 119.921
xres = 95.468

uwind = SlopeWind(inp, v, 697, yres, False)
saveloc = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Outputs\Poe Fire\vwindslope.csv"
np.savetxt(saveloc, uwind, delimiter=',')