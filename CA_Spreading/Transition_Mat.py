import numpy as np
import math
from numba import jit
import random
from CA_Spreading import CA_Definition as p

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

                for ell in range(L):
                    x = np.random.uniform(a / k, (a + 1) / k)
                    y = np.random.uniform(b / k, (b + 1) / k)
                    z = np.random.uniform(c / k, (c + 1) / k)
                    d = math.floor(k * H(x, y, z))
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

@jit(nopython = True)
def wind(arr, xwind, ywind, m, n):
    #x dir
    if xwind[m, n] > 0:
        x = (arr[m, n] - arr[m, n - 1])
    else:
        x = (arr[m, n + 1] - arr[m, n])

    #y dir
    if ywind[m, n] > 0:
        y = (arr[m + 1, n] - arr[m, n])
    else:
        y = (arr[m, n] - arr[m - 1, n])

    x = x * p.wfac * xwind[m, n]
    y = - y * p.wfac * ywind[m, n]

    return - 1/2 * (p.delt / p.delx) * (x + y)

@jit(nopython = True)
def slope(arr, xslp, yslp, m, n):
    #x dir
    if xslp[m, n] > 0:
        x = (arr[m, n] - arr[m, n-1])
    else:
        x = (arr[m, n + 1] - arr[m, n])

    #y dir
    if yslp[m, n] > 0:
        y = (arr[m + 1, n] - arr[m, n])
    else:
        y = (arr[m, n] - arr[m - 1, n])

    x = x * p.sfac * xslp[m, n]
    y = - y * p.sfac * yslp[m, n]

    return - 1/2 * (p.delt / p.delx) * (x + y)

@jit(nopython = True)
def update2D(arr, deturm, P, k, windarr, slparr):
    #loop for time steps
    t, m, n = arr.shape

    for time in range(1, t):
        for j in range(1, m-1):
            for ell in range(1, n-1):
                if time % 4 == 0:
                    alpha = int(arr[time - 1, j, ell - 1] * k ** 2 + arr[time - 1, j, ell] * k + arr[time - 1, j, ell + 1])
                    beta = int(arr[time - 1, j - 1, ell] * k ** 2 + arr[time - 1, j, ell] * k + arr[time - 1, j + 1, ell])
                elif time % 4 == 1:
                    alpha = int(arr[time - 1, j, ell + 1] * k ** 2 + arr[time - 1, j, ell] * k + arr[time - 1, j, ell - 1])
                    beta = int(arr[time - 1, j - 1, ell] * k ** 2 + arr[time - 1, j, ell] * k + arr[time - 1, j + 1, ell])
                elif time % 4 == 2:
                    alpha = int(arr[time - 1, j, ell + 1] * k ** 2 + arr[time - 1, j, ell] * k + arr[time - 1, j, ell - 1])
                    beta = int(arr[time - 1, j + 1, ell] * k ** 2 + arr[time - 1, j, ell] * k + arr[time - 1, j - 1, ell])
                else:
                    alpha = int(arr[time - 1, j, ell - 1] * k ** 2 + arr[time - 1, j, ell] * k + arr[time - 1, j, ell + 1])
                    beta = int(arr[time - 1, j + 1, ell] * k ** 2 + arr[time - 1, j, ell] * k + arr[time - 1, j - 1, ell])

                if deturm:
                    arr[ell, j] = 1/2 * (P[alpha, 0] + P[beta, 0])
                else:
                    prob1 = random.random()
                    prob2 = random.random()

                    arr[time, j, ell] = np.ceil(1/2 * (colcheck(prob1, alpha, P) + colcheck(prob2, beta, P)))

                    #wind and slope
                    windcor = wind(arr[time - 1, :, :], windarr[:, :, 0], windarr[:, :, 1], j, ell)
                    slopecor = slope(arr[time - 1, :, :], slparr[:, :, 0], slparr[:, :, 1], j, ell)
                    arr[time, j, ell] = round(arr[time, j, ell] + windcor + slopecor)
                    arr[time, j, ell] = max(min(arr[time, j, ell], k - 1), 0)

        # loop for array width (set up with neuman BC)
        arr[time, 0, :] = arr[0, 0, :]
        arr[time, -1, :] = arr[0, -1, :]
        arr[time, :, 0] = arr[0, :, 0]
        arr[time, :, -1] = arr[0, :, -1]

    return  arr