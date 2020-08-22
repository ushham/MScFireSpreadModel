import numpy as np
from FireSpotting import Ascent, FreeFall, Ignition
import matplotlib.pyplot as plt
import scipy.ndimage

class FireBrand:
    #Assumptions made on some paramters:
    minh = 10   #Min firebrand height escaping plume, any lower and we assume this is modelled in normal fire spread
    maxh = 1000 #Maximum firebrand altitude attaned. From Litrature, any higher and we are not expecting any firebrands to land.
    maxm = 0.03 #10g firebrand assumed as maximum loftable (from litrature).

    mid = 0.05   #Firebrand size which causes ignition 50% of the time
    skew = 1
    eta = 0.02
    w0 = 10

    mu= 0.005


    def __init__(self, lam, wx, num):
        self.lam = lam
        self.xwind = wx
        self.num = num

    def mass(self):
        #power law distribution for firebrand size
        size = np.random.exponential(self.mu, self.num)
        return size

    def loft(self):
        SubMod1 = Ascent.SubModel1(self.minh, self.maxh, self.lam, self.maxm)
        m = self.mass()
        holdr = np.empty(self.num)  #array to hold mass and escape height
        holdz = np.empty(self.num)
        icount = 0

        for i in m:
            #find height of each element
            pdf = np.array(SubMod1.PrdDist())
            h = np.random.choice(pdf[0, :], 1, p=pdf[1, :]/np.sum(pdf[1, :]))
            #r = (3/4 * i / (self.rho0 * np.pi)) ** (1/3)
            holdr[icount], holdz[icount] = i, h
            icount += 1

        return holdr, holdz

    def float(self, r0, z):
        SubMod2 = FreeFall.SubModel2(self.eta, self.w0, self.xwind)
        time = np.empty(self.num)
        rf = np.empty(self.num)
        for i in range(self.num):
            time[i] = SubMod2.ground(r0[i], z[i])
            rf[i] = SubMod2.r_r0(time[i], r0[i]) * r0[i]
            #print(r0, z, time[i], rf[i])

        return time, rf

    def dist(self, time, r0, z):
        SubMod2 = FreeFall.SubModel2(self.eta, self.w0, self.xwind)
        coordx = np.empty(self.num)
        for i in range(self.num):
            coordx[i] = SubMod2.coord(time[i], r0[i], z[i])[0]
        return coordx

    def lite(self, r):
        SubMod3 = Ignition.SubModel3(self.mid, self.skew)
        igprob = SubMod3.PDF(r)
        return igprob


#minh, maxh, lam, maxm

from matplotlib import ticker
from mpl_toolkits.axes_grid1 import make_axes_locatable

n=110
test = FireBrand(100, 1, 1)


z = np.linspace(800, 10, n)
r0 = np.linspace(0, 0.03, n)

rf = np.empty((n, n))
ic = 0
jc = 0
for i in z:
    jc = 0
    for j in r0:
        rf[ic, jc] = test.float([j], [i])[1][0] * j
        jc += 1
    ic += 1

xx, yy = np.meshgrid(r0, z)

#plt.scatter(xx, yy, c=rf)
print(np.round(rf, 3))
fig, ax = plt.subplots()
pt = plt.contourf(xx, yy, rf, cmap='RdGy')

plt.xlabel(r"Initial Radius $r_0$ (m)")
plt.ylabel(r"Height (m)")
plt.ylim(0, 400)
divider = make_axes_locatable(ax)

cax = divider.append_axes('right', size='3%', pad=0.2)
plt.colorbar(cax=cax)
cax.set_ylabel("Radius on Landing (m)")

plt.show()
###############################

# n = 1000000
# test = FireBrand(100, 10, n)
# lf = test.loft()
# fl = test.float(*lf)
#
# xdis = test.dist(fl[0], *lf)
# loc = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\CSVs\FireBrands\Firebrand-x-dir.csv"
# np.savetxt(loc, xdis, delimiter=',')
