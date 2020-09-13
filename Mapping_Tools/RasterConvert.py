import numpy as np
from osgeo import gdal
from osgeo import osr

#Exports csv as tif file
def Convert2tif(inputfile, dumploc, coord1, coord2, xsize, ysize, boolian):
    #Inputs: input file location, output folder, output name, coordinate top left, coordinate bottom right,_
    #   number of vertical and horizontal spacings, True if reading from file, false if given array

    if boolian:
        array = np.genfromtxt(inputfile, delimiter = ',')
    else:
        array = inputfile

    #Assign corrdinates, coord1 is top left corner, coord2 is bottom right
    lon = np.array((coord1[1], coord2[1]))
    lat = np.array((coord1[0], coord2[0]))

    #Calculate spacings between lat and long given
    xmin,ymin,xmax,ymax = [lon.min(),lat.min(),lon.max(),lat.max()]

    xres = (xmax-xmin)/float(xsize)
    yres = (ymax-ymin)/float(ysize)

    geotransform = (xmin, xres, 0, ymax, 0, -yres)
    # (top left x, w-e pixel resolution, rotation (0 if North is up),
    #         top left y, rotation (0 if North is up), n-s pixel resolution)

    fileloc = dumploc + '.tif'

    #Create raster file
    output_raster = gdal.GetDriverByName('GTiff').Create(fileloc, xsize, ysize, 1, gdal.GDT_Float32)
    output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
    srs = osr.SpatialReference()                 # Establish its coordinate encoding
    srs.ImportFromEPSG(4326)                     # Specifies WGS84 lat long.

    output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system
    output_raster.GetRasterBand(1).WriteArray(array)   # Writes my array to the raster
    output_raster.FlushCache()
    return 0

def readrst(loc):
    ds = gdal.Open(loc + ".tif")
    myarray = np.array(ds.GetRasterBand(1).ReadAsArray())

    return myarray