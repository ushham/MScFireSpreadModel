coord1 = (-35.66, 136.532)
coord2 = (-36.07, 136.955)

#only use for pure data extraction, not the running of the CA
xsize = 750
ysize = 750

datesin = []    #dates to extract data for in 'yyyy-mm-dd' format
times = []      #times to extract in 'hh:mm' format

saveloc = r''   #location for data to be saved to

#FileLocations
waterfolder = r''   #file location of surface water data
waterfile = ''      #file name

elefolder = r''     #file location of elevation data
elefile = ''        #file name

firefolder = r''    #file location of fire observation data
firefile = ''       #file name

weatherfolder = r'' #file location of GRIB data
weatherfile = ''    #file name

roadfolder = r''    #file location of road data
roadfile = ''       #file name

#Weather Data
hrspace = 12
startcoords = (-12, 111)

#Windspeed/hill length interaction
windfact = 0.1      #Parameter to allter effect of slope on wind speed
windhill = 8 / 5    #Calibrated Wind speed increase dependant on height
upperwindlim = 3    #Maximum windspeed increase from base

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

#Height Difference
delh = 50
