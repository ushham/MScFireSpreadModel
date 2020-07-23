#Basic parameters
coord1 = (-14.8142, 131.1556)
coord2 = (-15.1381, 131.5446)

xsize = 400
ysize = 400

datesin = ['2019-11-16', '2019-11-17', '2019-11-18', '2019-11-19', '2019-11-20', '2019-11-21']

saveloc = r'C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Outputs\North WA'

#Fire Data
hrspace = 12

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