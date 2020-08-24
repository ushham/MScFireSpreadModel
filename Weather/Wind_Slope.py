import numpy as np
from Control import Parameters


class WindTopography:
    def __init__(self, slope, wind, delh, res, bool):
        self.funcdata = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\CSVs\Slope-Wind\Slope-Wind 200711.csv"
        self.slope = slope
        self.wind = wind
        self.dh = delh
        self.res = res
        self.b = bool
        self.hillfact = self.res / (self.dh * Parameters.windhill) * Parameters.windfact

    def thetahold(self):
        return np.genfromtxt(self.funcdata, delimiter=',')

    def tau(self, theta, hold):
        #Function which returns increase in wind velocity due to slope
        #Assuming function is to 3 decimals of precision
        gap = hold[0, 1] - hold[0, 0]
        start = theta - hold[0, 0]
        loc = int(start / gap)
        return hold[1, loc] * self.hillfact + 1

    def Data_Extract(self):
        #Expects 2d array of slope and 2d array of wind at same resolution. true = u, false = v
        outarr = np.zeros(self.slope.shape)
        thetahold = self.thetahold()

        #to make range directions uniform, make v wind negitive (positive wind blows south)
        #Also set dimention

        if not(self.b):
            windop = -self.wind
            dim = 1
        else:
            dim = 0

        #take wind direction at left (u), top (v) of the wind array for each row/column to check
        #controlling wind direction
        for i in range(self.slope.shape[dim]):
            if self.b:
                startwin = self.wind[i, 0]
            else:
                startwin = windop[0, i]
            upperlim = abs(Parameters.upperwindlim * startwin)  # % increase allowed

            if startwin > 0:  #wind going left to right or top to bottom
                rng = range(0, self.slope.shape[1 - dim])    #increasing range
                side = - 1  #Direction upwind
            else:
                rng = range(self.slope.shape[1 - dim] - 1, -1, -1)   #decreasing range
                side = 1    #Direction upwind

            for j in rng:
                if self.b:
                    if j == rng[0]:
                        outarr[i, j] = startwin * self.tau(np.sign(startwin) * self.slope[i, j], thetahold)
                    else:
                        outarr[i, j] = outarr[i, j + side] * self.tau(np.sign(outarr[i, j + side]) * self.slope[i, j], thetahold)
                        outarr[i, j] = np.sign(outarr[i, j]) * min(upperlim, abs(outarr[i, j]))
                else:
                    if j == rng[0]:
                        outarr[j, i] = startwin * self.tau(np.sign(startwin) * self.slope[j, i], thetahold)
                    else:
                        outarr[j, i] = outarr[j + side, i] * self.tau(np.sign(outarr[j + side, i]) * self.slope[j, i], thetahold)
                        outarr[j, i] = np.sign(outarr[j, i]) * min(upperlim, abs(outarr[j, i]))

        return outarr
