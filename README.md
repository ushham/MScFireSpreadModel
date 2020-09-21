This project was undertaken as part of the disertation in part fulfilment of the MSc in Mathematical Modelling, taught at UCL (University College London).

The project models forest fire spread using Cellular Automata, taking into account: Wind, Topography, Firebreaks and Firebrands.

The code requires a number of data sources, and the locations of the data sourses need to be linked at `Control -> Parameters`.
These sourses can be found at the following locations:

Weather Data: [Climate Data Store](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form)

Surface Water Data: [European Commision Data Store](https://global-surface-water.appspot.com/download)  

Road Data: [Open Street Map, downloaded via Geofabrik](https://www.geofabrik.de/data/download.html)

Elevation Data: [GMTED2010 Database](https://topotools.cr.usgs.gov/gmted_viewer/viewer.htm)

Historic Fire Data: [NASA Earth Data](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/active-fire-data)



The folders contain the following key scripts:

Folder | Key Scripts | Purpose
------ | --------|--------
Control | Parameters | Definition of file locations, coordinates of fire, resolution of raster files to be produced.
Barriers | RoadData | Extracting road data from OpenStreetMap and creating raster file at defined resolution.
CA Spreading | CA_Definition & CA_Run | The parameters which control the spreading behaviour of the CA, and the script which runs the data extraction and running of the CA.
Elevations | ElevationData | Extraction and interpolation of elevation data, which outputs raster file.
Fire_Locations | FireData | Extract locations of fire observations from satellite data.
FireSpotting | CombinedModel | The three sub models described in the report are combined to produce a sample of locations where firebrands are expected to ignite fuel.
Surface_Water | WaterData | Extraction of surface water data, given the number of months per year water is identified to be at that location (default is 12 months).
Weather | Grib_Ext & Wind_Slope | Extraction of wind data from GRIB files at the specified time periods. This wind data is then modified using the topography as described in the report.
Mapping_Tools | - | Miscellaneous functions used to undertake calculations for mapping, or conversion of one data type to another 

Main developer: O Hamilton,

Supervisor: Prof. S Bishop