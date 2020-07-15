from CA_Spreading import Transition_Mat as mat
from Control import Parameters as p
import numpy as np

deturm = False
saveloc = p.saveloc + 'CA Outputs'

#stability check
check1 = (p.delx ** 2) / (2 * p.vee + p.kapa * (p.delx ** 2))
print('del t: ' + str(p.delt) + ' < ' + str(check1))

#Data holding array
arr = np.zeros((p.t, p.n, p.m))

print('Making probability transition matrix')

if deturm:
    pmat = np.genfromtxt(saveloc, delimiter=',')
else:
    pmat = mat.Pmaker(p.k, deturm, p.ell, mat.H)


print('running CA')

arr = mat.update(arr, deturm, pmat, p.k, 0)
print(arr)