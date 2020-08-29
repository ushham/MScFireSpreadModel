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
res = llt.Coord2Dist((pm.coord2[1] - pm.coord1[1]) / p.n, (pm.coord1[0] - pm.coord2[0]) / p.m, pm.coord1[0])
print("Grid Resolution in km (x, y): " + str(res))

#Wind Data Read in
winnum = len(pm.times) * len(pm.datesin)
windu = np.zeros((winnum, p.m, p.n), dtype=np.float32)
windv = np.zeros((winnum, p.m, p.n), dtype=np.float32)
if p.wthuse:   #check if there is weather data to extract
    for i in range(winnum):
        windu[i, :, :] = rc.readrst(pm.saveloc + "\\" + "WindData" + str(i) + "-u")
        windv[i, :, :] = -rc.readrst(pm.saveloc + "\\" + "WindData" + str(i) + "-v")    #negitive sign as wind direction is reverse of axis direction


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
    fbrk = np.ones((p.m, p.n), dtype=np.float32)

######### Step 2: define Spreading ####################:
print("Step 2: CA Details")
start = time.time()

#Calculate rate of spread
vee, gamma = tm.ROSdef(p.r0, p.theta).convert()

#stability check
check1 = (p.delx ** 2) / (2 * vee + gamma * (p.delx ** 2))
print('del t: ' + str(p.delt) + ' < ' + str(check1))

ini = p.k - 1

######### Step 3: Initial conditions ####################:

arr = np.zeros((p.t, p.m, p.n), dtype=np.float32)
#arr[0, 290:300, 370:380] = ini

arr[0, :, :] = rc.readrst(pm.saveloc + "\\Res hr+36") * (p.k - 1)

n=3
######### Step 4: Run CA ####################:
print("Step 4: Running CA")
print("Vee, Gamma:" + str(vee) + ", "+ str(gamma) )
hrsp = 24 // len(pm.times)

fb = fs.FireBrand(p.meanh, p.num).Collection(windu, windv, p.minrad, *res, p.shift)
np.savetxt(pm.saveloc + '\\FireBrands1.csv', fb[0, :, :], delimiter=',')
np.savetxt(pm.saveloc + '\\FireBrands2.csv', fb[1, :, :], delimiter=',')


ca = tm.RunCA(p.k, p.deturm, p.L, arr, windu, windv, slpx, slpy, fbrk, hrsp, vee, gamma)
#P = ca.Pmaker()
P = np.genfromtxt(pm.saveloc + '\\PMat.csv', delimiter=',')
arr = ca.update2D(P, fb, max(*res), n)

print('Saving CA')
rc.Convert2tif(arr[-1, :, :] / (p.k - 1), pm.saveloc + "\\Res hr+48", pm.coord1, pm.coord2, p.n, p.m, False)
np.savetxt(pm.saveloc + '\\PMat.csv', P, delimiter=',')

######### Step 5: Visualisation ####################:
print("Last Step: Making Animation")
vs.Visualisation(arr, fbrk, p.k, pm.saveloc + "\\" + "animationALLTESTfbtest").HeatMap(max(*res), 36)