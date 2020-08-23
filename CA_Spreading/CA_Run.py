import numpy as np
import time
from CA_Spreading import CA_Definition as p
from Mapping_Tools import RasterConvert as rc
from Mapping_Tools import LatLongTools as llt
from CA_Spreading import Transition_Mat as tm
from CA_Spreading import CA_Vis as vs
from CA_Spreading import CA_Data as cd
from Control import Parameters as pm
from FireSpotting import CombinedModel as fs


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

xres, yres = llt.Coord2Dist((pm.coord2[1] - pm.coord1[1]) / p.n, (pm.coord1[0] - pm.coord2[0]) / p.m, pm.coord1[0])

######### Step 3: Initial conditions ####################:

arr = np.zeros((p.t, p.m, p.n), dtype=np.float32)
arr[0, 480:500, 280:320] = ini

######### Step 4: Run CA ####################:
print("Step 4: Running CA")
hrsp = 24 // len(pm.times)

fb = fs.FireBrand(p.meanh, p.num).Collection(windu, windv, p.minrad, xres, yres, p.shift, len(pm.times))

ca = tm.RunCA(p.k, p.deturm, p.L, arr, windu, windv, slpx, slpy, fbrk, hrsp)
arr = ca.update2D(ca.Pmaker(), fb)
print('Running CA')


######### Step 5: Visualisation ####################:
print("Last Step: Making Animation")
vs.Visualisation(arr, fbrk, p.k, pm.saveloc + "\\" + "animationALLTESTfbtest").HeatMap()