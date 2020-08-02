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

        if startwin > 0:  #wind going left to right
            rng = range(0, slope.shape[1 - dim])
            side = - 1
        else:
            rng = range(slope.shape[1 - dim] - 1, -1, -1)
            side = 1


        for j in rng:
            if bool:
                if i == rng[0]:
                    outarr[i, j] = wind * tau(slope[i, j], hillfact)
                else:
                    outarr[i, j] = outarr[i, j + side] * tau(slope[i, j], hillfact)
            else:
                if i == rng[0]:
                    outarr[j, i] = wind * tau(slope[j, i], hillfact)
                else:
                    outarr[j, i] = outarr[i + side, j] * tau(slope[j, i], hillfact)

    return outarr
