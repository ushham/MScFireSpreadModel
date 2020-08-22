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
brkuse = True       #break data


k = 20        #Number of states of CA

L = 10000        #Number of Trials to make transition matrix


delx = 1      #CA variables
delt = 1        #Time steps = 1 / minute
vee = 0.05      #spreading factor
gamma = 0.05        #growth factor


n = 300         #size of array
m = 300
t = 500

wfac = 0
sfac = 0.5


#Vis parameters
tts = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, -1]
