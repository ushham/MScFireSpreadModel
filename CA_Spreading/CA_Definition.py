deturm = False  #Determanistic CA?
savedmat = False
k = 20        #Number of states of CA

L = 10000        #Number of Trials to make transition matrix


delx = 1      #CA variables
delt = 1
vee = 0.05      #spreading factor
gamma = 0.05        #growth factor


n = 100         #size of array
m = 100
t = 1000

wfac = 0.5
sfac = 0

#date for wind data
dates = ['2019-12-21', '2019-12-22', '2019-12-23', '2019-12-24', '2019-12-25', '2019-12-26', '2019-12-27']
times = ['00:00', '12:00']

#Vis parameters
tts = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
