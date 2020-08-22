import numpy as np
from FireSpotting import Ascent, FreeFall, Ignition

class FireBrand:
    #Assumptions made on some paramters:
    minh = 10   #Min firebrand height escaping plume, any lower and we assume this is modelled in normal fire spread
    maxh = 1000 #Maximum firebrand altitude attaned. From Litrature, any higher and we are not expecting any firebrands to land.
    maxm = 0.03 #10g firebrand assumed as maximum loftable (from litrature).

    mid = 0.05   #Firebrand size which causes ignition 50% of the time
    skew = 1
    eta = 0.005
    w0 = 16

    mu= 0.005


    def __init__(self, lam, num):
        self.lam = lam
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

    def float(self, r0, z, wx):
        SubMod2 = FreeFall.SubModel2(self.eta, self.w0, wx)
        time = np.empty(self.num)
        rf = np.empty(self.num)
        for i in range(self.num):
            time[i] = SubMod2.ground(r0[i], z[i])
            rf[i] = SubMod2.r_r0(time[i], r0[i]) * r0[i]

        return time, rf

    def dist(self, time, r0, z, wx):
        SubMod2 = FreeFall.SubModel2(self.eta, self.w0, wx)
        coordx = np.empty(self.num)
        for i in range(self.num):
            coordx[i] = SubMod2.coord(time[i], r0[i], z[i])[0]
        return coordx

    def lite(self, r):
        SubMod3 = Ignition.SubModel3(self.mid, self.skew)
        igprob = SubMod3.PDF(r)
        return igprob


    def journey(self, wx, wy, p0, xres, yres, shift):
        r, z = self.loft()
        t, rf = self.float(r, z, wx)
        x = self.dist(t, r, z, wx)
        y = self.dist(t, r, z, wy)
        p = self.lite(rf)

        #return only interesting points
        filt = ~np.isnan(p)
        x = x[filt]
        y = y[filt]
        x = x[p[filt] >= p0]
        y = y[p[filt] >= p0]

        # find distance off centre-line
        angle = np.random.normal(0, shift, x.shape[0])
        xoffc = x * np.tan(2 * np.pi * angle / 360)
        yoffc = y * np.tan(2 * np.pi * angle / 360)

        x = np.round(x / xres)
        y = np.round(y / yres)
        xoffc = np.round(xoffc / xres)
        yoffc = np.round(yoffc / yres)

        filt = np.logical_or(x > 0, y > 0)

        xoffc = xoffc[filt]
        yoffc = yoffc[filt]
        x = x[filt]
        y = y[filt]
        print(x, y)

        return x + yoffc, y + xoffc

test = FireBrand(400, 100)

#wx, wy, p0, xres, yres, shift
print(test.journey(5, 2, 0.4, 50, 50, 10))

