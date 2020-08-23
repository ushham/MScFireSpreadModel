deturm = False  #Determanistic CA?
savedmat = False

# Updating Data sources on/off
ele = False     #elevation data
wth = False     #weather data
wat = False     #water data
rod = False     #road data

# Using Data sources on/off
eleuse = True     #elevation data
wthuse = True     #weather data
brkuse = True     #break data
frbuse = True     #Firebrand sim


k = 20        #Number of states of CA

L = 10000        #Number of Trials to make transition matrix


delx = 1      #CA variables
delt = 1        #Time steps = 1 / minute
vee = 0.05      #spreading factor
gamma = 0.05        #growth factor


n = 800         #size of array
m = 800
t = 600

wfac = 0.15
sfac = 0.5


#Vis parameters
tts = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, -1]


#Firebrand Parimiters
minKval = 0
maxKval = int(3 * k / 4)

meanh = 200
num = 100

shift = 5   #Standard deviation of wind shifts in degrees
minrad = 0.001  #min radius that can start fire