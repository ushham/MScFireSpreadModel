from CA_Spreading import CA_Definition as d
from Control import Parameters as p
from Weather import Wind_Data as wnd
from datetime import datetime

coord = (p.coord1, p.coord2)

#Modified wind data
wethloc = p.weatherfolder + '\\' + p.weatherfile

reppday = 1
for date in d.dates:
    for time in d.times:
        print(datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M'))
        tim = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
        wnd.WindDat(wethloc, '', p.dt, tim, p.startcoords, coord[0], coord[1], d.m, d.n)

