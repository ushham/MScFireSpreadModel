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
    #Expects 2d array of slope and 2d array of wind at same resolution. true = u, false = v

    #delh - hill length - grid resolution:
    ell = delh * Parameters.windhill
    hillfact = res / ell

    outarr = np.zeros(slope.shape)

    #to make range directions uniform, make v wind negitive (positive wind blows south)
    #Also set dimention

    if not(bool):
        wind = -wind
        dim = 1
    else:
        dim = 0

    #take wind direction at left (u), top (v) of the wind array for each row/column to check
    #controlling wind direction
    for i in range(slope.shape[dim]):
        if bool:
            startwin = wind[i, 0]
        else:
            startwin = wind[0, i]
        upperlim = abs(Parameters.upperwindlim * startwin)  # % increase allowed

        if startwin > 0:  #wind going left to right or top to bottom
            rng = range(0, slope.shape[1 - dim])    #increasing range
            side = - 1  #Direction upwind
        else:
            rng = range(slope.shape[1 - dim] - 1, -1, -1)   #decreasing range
            side = 1    #Direction upwind

        for j in rng:
            if bool:
                if j == rng[0]:
                    outarr[i, j] = startwin * tau(np.sign(startwin) * slope[i, j], hillfact)
                else:
                    outarr[i, j] = outarr[i, j + side] * tau(np.sign(outarr[i, j + side]) * slope[i, j], hillfact)
                    outarr[i, j] = np.sign(outarr[i, j]) * min(upperlim, abs(outarr[i, j]))
            else:
                if j == rng[0]:
                    outarr[j, i] = startwin * tau(np.sign(startwin) * slope[j, i], hillfact)
                else:
                    outarr[j, i] = outarr[j + side, i] * tau(np.sign(outarr[j + side, i]) * slope[j, i], hillfact)
                    outarr[j, i] = np.sign(outarr[j, i]) * min(upperlim, abs(outarr[j, i]))

    return outarr
