import numpy as np
from numba import jit
import time
from CA_Spreading import CA_Definition as p
from CA_Spreading import Transition_Mat as tm
from CA_Spreading import CA_Vis as vs

fileloc = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\CA Testing\Results\Fisher\LTesting\\'

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

################# Wind and Slope ##############################
wind = np.zeros((p.m, p.n, 2))
wind[:, :, 1] = -1

slp = np.zeros((p.m, p.n, 2))

arr = np.zeros((p.t, p.m, p.n))
arr[0, 45:50, 45:50] = ini

P = tm.Pmaker(p.k, p.deturm, p.L, H)

print('running CA')
arr = tm.update2D(arr, p.deturm, P, p.k, wind, slp)

arrshow = np.empty((len(p.tts), p.m, p.n))

icount = 0
for i in p.tts:
    arrshow[icount, :, :] = arr[i, :, :]
    icount += 1

vs.HeatMap(arrshow, p.k)


