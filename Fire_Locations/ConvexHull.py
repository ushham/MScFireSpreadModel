import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from Mapping_Tools import RasterConvert as rc

def CreateSurface(fileloc, filename, dumploc, coord1, coord2, sizex, sizey, boolian):
    #Opens file, or expected df to be passed, and returns a sursafe of expected fire based on FRP
    #Saves a raster of surface
    #constants
    lat = 'LATITUDE'
    long = 'LONGITUDE'
    conf = 'FRP'

    #checks if file or df is passed
    if boolian:
        firedata = pd.read_csv(fileloc + '\\' + filename)
    else:
        firedata = fileloc

    #set size of arrays
    points = np.array(firedata[[lat, long]])
    delx = abs(coord1[1] - coord2[1]) / sizex
    dely = abs(coord1[0] - coord2[0]) / sizey

    #create evenly spaced array given number of boxes
    x = np.arange(min(coord1[1], coord2[1]), max(coord1[1], coord2[1]), delx)
    y = np.arange(max(coord1[0], coord2[0]), min(coord1[0], coord2[0]), -dely)

    grid_x, grid_y = np.meshgrid(x, y)

    pointy = points[:, 0]
    pointx = points[:, 1]

    #create surface
    #Check if there are enough points to make surface
    if len(firedata.index) >= 4:
        z = griddata((pointx, pointy), firedata[conf], (grid_x, grid_y), method='linear')
        #Convert surface to raster file
        rc.Convert2tif(z, dumploc, coord1, coord2, sizex, sizey, False)
    else:
        print('Not enough points at ' + dumploc)
    return 0

