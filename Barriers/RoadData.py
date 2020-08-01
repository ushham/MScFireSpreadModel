import numpy as np
import gdal as gd
import geopandas as gpd
from osgeo import ogr
import rasterio as rs
import shapefile


def TrimShp(loc, coord1, coord2, saveloc):
    r = shapefile.Reader(loc)
    print(r)
    save = saveloc + "\\" + "shpTest"
    w = shapefile.Writer(save, r.shapeType)

    w.fields = list(r.fields)

    xmin = coord1[1]
    xmax = coord2[1]
    ymin = coord2[0]
    ymax = coord1[0]

    #Iterate thorugh shapes and attributes at same time
    for road in r.iterShapeRecords():
        # Shape geometry
        geom = road.shape

        # Database attributes
        rec = road.record

        # Get the bounding box of the shape (a single road)
        sxmin, symin, sxmax, symax = geom.bbox
        # Compare it to our Puerto Rico bounding box.
        # go to the next road as soon as a coordinate is outside the box
        if sxmin < xmin: continue
        elif sxmax > xmax: continue
        elif symin < ymin: continue
        elif symax > ymax: continue
        # Road is inside our selection box.
        # Add it to the new shapefile
        print(geom, rec)
        w._shapes.append(geom)
        w.records.append(rec)
    w.save(save)
    return 0

def RoadLoc(loc, coord1, coord2, xres, yres, saveloc):
    #Convert the shp file to a raster and then export to
    #tif or array

    #open data and extract layer at specified area
    roads = gd.ogr.Open(loc)
    roadlr = roads.GetLayer()

    bound = "POLYGON ((%f %f, %f %f, %f %f, %f %f, %f %f))" %(coord1[1], coord1[0], coord1[1], coord2[0], coord2[1], coord2[0], coord2[1], coord1[0], coord1[1], coord1[0])
    print(bound)

    roadlr.SetSpatialFilter(ogr.CreateGeometryFromWkt(bound))

    road_srs = roadlr.GetSpatialRef()
    print(roadlr.GetExtent())

    #grid size (arc degrees)
    xlen = (coord2[1] - coord1[1]) / xres
    ylen = (coord2[0] - coord1[0]) / yres

    out_driver = gd.GetDriverByName('GTiff')

    tiffloc = saveloc + "\\" + "TiffTest.tif"

    out_source = out_driver.Create(tiffloc, xres, yres, 1, gd.GDT_CInt16)
    out_source.SetGeoTransform((coord1[1], xlen, 0, coord1[0], 0, ylen))
    out_source.SetProjection(road_srs.ExportToWkt())
    out_lyr = out_source.GetRasterBand(1)
    out_lyr.SetNoDataValue(-9999)

    #Convert to Raster
    gd.RasterizeLayer(out_source, [1], roadlr, burn_values=[1])
    return 0



    # roads = gp.read_file(loc)
    # loc_roads = roads.cx[coord1[1]:coord2[1], coord1[0]:coord2[0]]


    #create boundary box


loc = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Road Data\Australia\australia-latest-free.shp\gis_osm_roads_free_1.shp"
op = r"C:\Users\UKOGH001\Documents\03 Masters\10 Project\GIS\Road Data\Australia\Tests"

coord1 = (-37.5, 143.78)
coord2 = (-37.62, 143.92)


#RoadLoc(loc, coord1, coord2, 200, 200, op)
TrimShp(loc, coord1, coord2, op)