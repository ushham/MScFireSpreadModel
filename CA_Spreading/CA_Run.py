import numpy as np
from numba import jit
import time
from CA_Spreading import CA_Definition as p
from Mapping_Tools import RasterConvert as rc
from CA_Spreading import Transition_Mat as tm
from CA_Spreading import CA_Vis as vs
from CA_Spreading import CA_Data as cd
from Control import Parameters as pm

cd.RunData()
print('DataGrab Complete')


start = time.time()
#stability check
check1 = (p.delx ** 2) / (2 * p.vee + p.gamma * (p.delx ** 2))
print('del t: ' + str(p.delt) + ' < ' + str(check1))

ini = p.k - 1
K = p.vee * p.delt / p.delx ** 2

################# Definition of Spread (forward Eular) ##########
@jit(nopython = True)
def H(x, y, z):
    n = y + K * (x - 2 * y + z) + p.delt * p.gamma * y * (1 - y)
    return n


#Wind Data Read in
winnum = len(pm.times) * len(pm.datesin)
windu = np.zeros((winnum, p.m, p.n))
windv = np.zeros((winnum, p.m, p.n))
if p.wthuse:   #check if there is weather data to extract
    for i in range(winnum):
        windu[i, :, :] = rc.readrst(pm.saveloc + "\\" + "WindData" + str(i) + "-u")
        windv[i, :, :] = rc.readrst(pm.saveloc + "\\" + "WindData" + str(i) + "-v")


#check if there is elevation data
slp = np.zeros((p.m, p.n, 2))
if p.eleuse:
    slpx = np.genfromtxt(pm.saveloc + "\\" + "xslope.csv", delimiter=",")
    slpy = np.genfromtxt(pm.saveloc + "\\" + "yslope.csv", delimiter=",")


#check if to use fire break:
if p.brkuse:
    fbrk = rc.readrst(cd.barriersav)
else:
    fbrk = None


arr = np.zeros((p.t, p.m, p.n))
arr[0, 230:240, 120:130] = ini

P = tm.Pmaker(p.k, p.deturm, p.L, H)

print('Running CA')
hrsp = 24 // len(pm.times)
arr = tm.update2D(arr, p.deturm, P, p.k, windu, windv, slpx, slpy, fbrk, hrsp)

arrshow = np.empty((len(p.tts), p.m, p.n))

icount = 0
# for i in p.tts:
#     arrshow[icount, :, :] = arr[i, :, :]
#     icount += 1

print("Making Animation")
vs.HeatMap(arr, fbrk, p.k, cd.anisav)