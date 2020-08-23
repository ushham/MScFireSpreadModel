import numpy as np
import gdal as gd
import shapefile

class RoadData:
    def __init__(self, loc, coord1, coord2, saveloc, xres, yres):
        self.fileloc = loc
        self.top_left = coord1
        self.bot_right = coord2
        self.saveloc = saveloc
        self.xres = xres
        self.yres = yres

        self.save = saveloc + "\\" + "LocalisedRoads"


    def TrimShp(self):
        # Create a reader instance for our US Roads shapefile
        r = shapefile.Reader(self.fileloc)

        # Create a writer instance copying the reader's shapefile type
        w = shapefile.Writer(self.save, r.shapeType)

        # Copy the database fields to the writer
        w.fields = list(r.fields)

        # Our selection box
        xmin, xmax, ymin, ymax = *self.top_left, *self.bot_right

        # Iterate through the shapes and attributes at the same time
        for road in r.iterShapeRecords():
            # Shape geometry
            geom = road.shape
            # Database attributes
            rec = road.record
            # Get the bounding box of the shape (a single road)
            sxmin, symin, sxmax, symax = geom.bbox
            # Compare it to our bounding box.
            # go to the next road as soon as a coordinate is outside the box
            if sxmin < xmin:
                continue
            elif sxmax > xmax:
                continue
            elif symin < ymin:
                continue
            elif symax > ymax:
                continue
            # Road is inside our selection box.
            # Add it to the new shapefile

            w.shape(geom)
            w.record(*rec)
        return 0


    def shp2rst(self):
        #Convert the shp file to a raster and then export to
        #tif or array

        #open data and extract layer at specified area
        roads = gd.ogr.Open(self.fileloc)
        roadlr = roads.GetLayer()


        #grid size (arc degrees)
        xlen = (self.bot_right[1] - self.top_left[1]) / self.xres
        ylen = (self.bot_right[0] - self.top_left[0]) / self.yres

        out_driver = gd.GetDriverByName('GTiff')

        tiffloc = self.saveloc + "\\" + "RoadRaster.tif"

        out_source = out_driver.Create(tiffloc, self.xres, self.yres, 1, gd.GDT_Float32)
        out_source.SetGeoTransform((self.top_left[1], xlen, 0, self.bot_right[0], 0, ylen))
        #out_source.SetProjection(road_srs.ExportToWkt())
        out_lyr = out_source.GetRasterBand(1)
        out_lyr.Fill(0)

        #Convert to Raster
        gd.RasterizeLayer(out_source,  # output to our new dataset
                                     [1],  # output to our new dataset's first band
                                     roadlr,  # rasterize this layer
                                     burn_values=[0],  # burn value 0
                                     options=['ALL_TOUCHED=TRUE', 'ATTRIBUTE=code']  # put raster values according to the 'id' field values
                                     )
        return tiffloc

    def roadrst(self, loc):
        ds = gd.Open(loc)
        myarray = np.array(ds.GetRasterBand(1).ReadAsArray())
        #alters array to retun 0 where roads are present, 1 where not
        myarray = np.where(myarray == 0 , 1, myarray)
        myarray = np.where(myarray != 1 , 0, myarray)

        return myarray

