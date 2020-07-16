#Basic parameters
coord1 = (-25, 152.4)
coord2 = (-25.2, 152.7)

xsize = 400
ysize = 400

datesin = ['2019-11-12', '2019-11-13', '2019-11-14', '2019-11-15', '2019-11-16']

saveloc = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Outputs\Woodgate Beach'

#Fire Data
hrspace = 3

#Windspeed/hill length interaction
windhill = 8 / 5
upperwindlim = 10

#CA Parameters
k = 10          #number of CA states
ell = 10000       #number of trials for Transition matrix

delx = 1        #size of step
delt = 0.08     #size of time step
vee = 0.5       #spread constant
kapa = 0.8      #growth constant

#array sizes
n = ysize
m = xsize
t = 10