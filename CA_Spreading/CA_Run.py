import numpy as np
from numba import jit
import time
from CA_Spreading import CA_Definition as p
from Mapping_Tools import RasterConvert as rc
from CA_Spreading import Transition_Mat as tm
from CA_Spreading import CA_Vis as vs
from CA_Spreading import CA_Data as cd
from Control import Parameters as pm


######### Step 1: Run Data Grab ####################:
print("Step 1: Extracting Data")
cd.RunData().ExtractAll()

#Wind Data Read in
winnum = len(pm.times) * len(pm.datesin)
windu = np.zeros((winnum, p.m, p.n), dtype=np.float32)
windv = np.zeros((winnum, p.m, p.n), dtype=np.float32)
if p.wthuse:   #check if there is weather data to extract
    for i in range(winnum):
        windu[i, :, :] = rc.readrst(pm.saveloc + "\\" + "WindData" + str(i) + "-u")
        windv[i, :, :] = rc.readrst(pm.saveloc + "\\" + "WindData" + str(i) + "-v")


#check if there is elevation data
print("Grabbing Slope Data")
if p.eleuse:
    slpx = np.genfromtxt(pm.saveloc + "\\" + "xslope.csv", delimiter=",", dtype=np.float32)
    slpy = np.genfromtxt(pm.saveloc + "\\" + "yslope.csv", delimiter=",", dtype=np.float32)
else:
    slpx, slpy = np.zeros((p.m, p.n), dtype=np.float32), np.zeros((p.m, p.n), dtype=np.float32)


#check if to use fire break:
print("Grabbing Firebrand Data")
if p.brkuse:
    fbrk = rc.readrst(pm.saveloc + "\\" + "FireBreaks")
else:
    fbrk = None

######### Step 2: define Spreading ####################:
print("Step 2: CA Details")
start = time.time()
#stability check
check1 = (p.delx ** 2) / (2 * p.vee + p.gamma * (p.delx ** 2))
print('del t: ' + str(p.delt) + ' < ' + str(check1))

ini = p.k - 1


######### Step 3: Initial conditions ####################:

arr = np.zeros((p.t, p.m, p.n), dtype=np.float32)
arr[0, 230:240, 120:130] = ini

######### Step 4: Run CA ####################:
print("Step 4: Running CA")
hrsp = 24 // len(pm.times)

ca = tm.RunCA(p.k, p.deturm, p.L, arr, windu, windv, slpx, slpy, fbrk, hrsp)

arr = ca.update2D(ca.Pmaker())
print('Running CA')


arrshow = np.empty((len(p.tts), p.m, p.n))

icount = 0
# for i in p.tts:
#     arrshow[icount, :, :] = arr[i, :, :]
#     icount += 1
######### Step 5: Visualisation ####################:
print("Last Step: Making Animation")
vs.Visualisation(arr, fbrk, p.k, pm.saveloc + "\\" + "animationALLTEST").HeatMap()