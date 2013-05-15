from osgeo import gdal, ogr, osr

spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +over +no_defs')

#Fields
width_field = ogr.FieldDefn( "width", ogr.OFTReal )
width_field.SetWidth( 32 )
driver = ogr.GetDriverByName("ESRI Shapefile")
road_file = "shape_roads.shp"
ds_roads = driver.CreateDataSource(road_file)
road_layer = ds_roads.CreateLayer('road', spatialReference, ogr.wkbLineString)
if road_layer.CreateField ( width_field ) != 0:
    print "Creating mat_id field failed.\n"

width = 15.0
lineString = [(327.34, 750.0), (331.74, 742.15), (337.28, 735.06), (342.03, 727.41), (349.44, 722.3), (357.02, 717.46), (364.6, 712.6), (371.34, 706.63), (376.18, 699.04), (381.69, 691.93), (387.77, 685.3), (391.79, 677.24), (397.03, 669.93), (402.56, 662.83), (404.78, 654.11), (404.57, 645.11), (402.51, 636.35), (404.45, 627.56), (404.92, 618.57), (409.15, 610.63), (413.47, 602.73), (414.86, 593.84), (416.6, 585.01), (421.91, 577.74), (429.27, 572.56), (436.12, 566.73), (440.69, 558.97)]

print 'add road'
road_feat = ogr.Feature( road_layer.GetLayerDefn())
print 1
road_feat.SetField( "width", width )
print 2
road_line = ogr.Geometry(ogr.wkbLineString)
print 3
for point in lineString:
    print 'add point'
    road_line.AddPoint(0, point[0], point[1])

road_feat.SetGeometry(road_line)
if road_layer.CreateFeature(road_feat) != 0:
    print "Failed to create feature in shapefile.\n"
    sys.exit( 1 )

road_feat.Destroy()