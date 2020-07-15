import numpy as np
import math
from numba import jit
import random
from CA_Spreading import CA_Definition as var

################# Definition of Spread (forward Eular) ##########
@jit(nopython = True)
def H(x, y, z):
    C = var.vee * var.delt / var.delx ** 2
    n = y + C * (x - 2 * y + z) + var.kapa * var.delt * y * (1 - y)
    return n


############## Make Transition Matrix ############
@jit(nopython = True)
def Pmaker(k, deturm, L, H):
    A = range(k)
    P = np.zeros((k ** 3, k))
    for a in A:
        for b in A:
            for c in A:
                alpha = a * (k ** 2) + (b * k) + c
                X = np.zeros(k)
                d = 0
                for ell in range(L):
                    x = np.random.uniform(a / k, (a + 1) / k)
                    y = np.random.uniform(b / k, (b + 1) / k)
                    z = np.random.uniform(c / k, (c + 1) / k)
                    d = math.floor(k * H(x, y, z))
                    #d = min(d, (k-1))
                    X[d] += 1

                if deturm:
                    P[alpha, 0] = np.argmax(X)
                else:
                    for i in A:
                        if np.sum(X[:]) == 0:
                            print(a, b, c, d)
                        if a == b == c == 0: #unstable equilibria exceptions:
                            P[alpha, i] = 1
                        else:
                            P[alpha, i] = X[i] / np.sum(X[:]) + (P[alpha, i - 1] if i > 0 else 0)
    return P


######## Returns column which refers to element with probability prob
@jit(nopython = True)
def colcheck(prob, x, P):
    i = 0
    while prob > P[x, i]:
        i += 1
    return i

######## Correction for wind and slope ####################
def coor(arr, t, i, j):
    windarr = ...
    slopearr = ...

    windconst = ...
    slopeconst = ...

    step = var.delx

    wind = 1/2 * windconst * windarr[t, i, j] * ((arr[t, i, j] - arr[t, i - 1, j]) / step + (arr[t, i, j] - arr[t, i, j - 1]) / step)
    slope = 1/2 * slopeconst * slopearr[t, i, j] * ((arr[t, i + 1, j] - arr[t, i, j]) / step + (arr[t, i, j] - arr[t, i, j - 1]) / step)

    return wind + slope

######## Returns completed CA for all time steps (2D) ##############
@jit(nopython=True)
def update(arr, deturm, P, k, coor):
    # loop for time steps
    # time steps
    t, n, m = arr.shape
    for ell in range(1, t):

        for i in range(1, n - 1):
            for j in range(1, m - 1):
                alpha = int(arr[ell - 1, i - 1, j] * k ** 2 + arr[ell - 1, i, j] * k + arr[ell - 1, (i + 1) % n, j])
                beta = int(arr[ell - 1, i, j - 1] * k ** 2 + arr[ell - 1, i, j] * k + arr[ell - 1, i, (j + 1) % m])
                if deturm:
                    arr[ell, i, j] = 1/2 * (P[alpha, 0] + P[beta, 0]) #+ coor(arr, t, i, j)
                else:
                    prob = random.random()
                    arr[ell, j, ell] = 1/2 * (colcheck(prob, alpha, P) + colcheck(prob, beta, P)) #+ coor(arr, t, i, j)
            # loop for array width (set up with derilect BC)
            arr[ell, 0, :] = arr[0, 0, :]
            arr[ell, -1, :] = arr[0, -1, :]
            arr[ell, :, 0] = arr[0, :, 0]
            arr[ell, :, -1] = arr[0, :, -1]

    return arr