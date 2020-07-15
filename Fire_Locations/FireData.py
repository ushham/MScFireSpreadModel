import geopandas as gpd
from datetime import datetime
from datetime import time
from Fire_Locations import ConvexHull as ch


def HourInt(intervals):
    #Returns array of times, given the hourly interval
    day2hour = 24
    intervals = min(day2hour, intervals)    #max hourly gap is 1 day

    numit = int(day2hour / intervals)
    timeint = []
    for i in range(numit):
        timeint.append(time(hour = int(i * day2hour / numit), minute = 0))
    
    timeint.append(time(hour = 23, minute = 59))    #end of day is added
    return timeint


def FireLayerExtract(loc, coord1, coord2, dumploc, hours, date, savedata):
    # Returns file of fire records within given area, on date within time band
    # constants
    firetime = 'ACQ_TIME'
    firedate = 'ACQ_DATE'
    firelat = 'LATITUDE'
    firelong = 'LONGITUDE'

    # Data Input file location
    firedf = gpd.read_file(loc)

    # calculates fire times
    timemin = hours[0]
    timemax = hours[1]

    # filters dataframe for only fires within the location box
    firedf = firedf[(firedf[firelat] < coord1[0]) & (firedf[firelat] > coord2[0])]
    firedf = firedf[(firedf[firelong] > coord1[1]) & (firedf[firelong] < coord2[1])]

    firedf[firetime] = firedf[firetime].apply(lambda x: datetime.strptime(x, '%H%M')).dt.time

    dttemp = firedf[(firedf[firedate] == date)]
    dttimetemp = dttemp[(dttemp[firetime] >= timemin) & (dttemp[firetime] <= timemax)]
    if dttimetemp.shape[0] > 0:
        dttimetemp = dttimetemp.drop([firetime], axis=1)
        if savedata:
            saveloc = dumploc + '\\' + str(date) + '-' + str(timemin).zfill(2) + '.csv'
            dttimetemp.to_csv(saveloc)
            out = 0
            run = False
        else:
            out = dttimetemp
            run = True
    else:
        out = 0
        run = False

    return run, out

def IterateFire(loc, saveloc, hrspace, datesin, coord1, coord2, xsize, ysize):
    time = HourInt(hrspace)
    for i in datesin:
        for j in range(len(time) - 1):
            timeint = [time[j], time[j+1]]
            run, firedat = FireLayerExtract(loc, coord1, coord2, saveloc, timeint, i, False)
            if run:
                dumploc = saveloc + '\\' + str(i) + '-' + str(time[j])[0:2]
                print(dumploc)
                ch.CreateSurface(firedat, '', dumploc, coord1, coord2, xsize, ysize, False)