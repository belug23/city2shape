import os

from osgeo import gdal, ogr, osr


class CityConverter(object):

    def __init__(self, directory, filename, position):
        self.directory = directory
        self.filename = filename
        self.position_correction = position
        self.filepath = '%s%s%s' % (directory, os.sep, filename)



    def convert(self, ):
        if not os.path.isfile(self.filepath):
            print self.filepath
            return False


        self.extract_name, ext = os.path.splitext(self.filename)

        if os.path.isdir(self.directory):
            target_dir = "%s%s%s" % (self.directory, os.sep, self.extract_name)

            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
                self.output_dir = target_dir
            else:
                copy_num = 2
                new_target = "%s %d" % (target_dir, copy_num)
                while os.path.exists(new_target):
                    copy_num += 1
                    new_target = "%s %d" % (target_dir, copy_num)

                os.mkdir(new_target)
                self.output_dir = new_target

        spatialReference = osr.SpatialReference()
        spatialReference.ImportFromProj4('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +over +no_defs')

        #Fields
        self.width_field = ogr.FieldDefn( "width", ogr.OFTReal )
        self.width_field.SetWidth( 32 )
        self.visible_field = ogr.FieldDefn( "visible", ogr.OFTInteger )
        self.visible_field.SetWidth( 32 )

        #driver = ogr.Driver("ESRI Shapefile")
        self.road_driver = ogr.GetDriverByName("ESRI Shapefile")
        road_file = "%s%s%s_roads.shp" % (self.output_dir, os.sep, self.extract_name)
        self.ds_roads = self.road_driver.CreateDataSource(road_file)
        self.road_layer = self.ds_roads.CreateLayer('road', spatialReference, ogr.wkbLineString)
        if self.road_layer.CreateField ( self.width_field ) != 0:
            print "Creating mat_id field failed.\n"
            return False
        self.road_def = self.road_layer.GetLayerDefn()

        self.river_driver = ogr.GetDriverByName("ESRI Shapefile")
        river_file = "%s%s%s_rivers.shp" % (self.output_dir, os.sep, self.extract_name)
        self.ds_rivers = self.river_driver.CreateDataSource(river_file)
        self.river_layer = self.ds_rivers.CreateLayer('river', spatialReference, ogr.wkbLineString)
        if self.river_layer.CreateField ( self.width_field ) != 0:
            print "Creating mat_id field failed.\n"
            return False
        self.river_def = self.river_layer.GetLayerDefn()

        ogr.Feature( self.river_def )

        self.lake_driver = ogr.GetDriverByName("ESRI Shapefile")
        lake_file = "%s%s%s_lakes.shp" % (self.output_dir, os.sep, self.extract_name)
        self.ds_lakes = self.lake_driver.CreateDataSource(lake_file)
        self.lake_layer = self.ds_lakes.CreateLayer('lake', spatialReference, ogr.wkbPolygon)
        self.lake_def = self.lake_layer.GetLayerDefn()

        self.building_driver = ogr.GetDriverByName("ESRI Shapefile")
        building_file = "%s%s%s_buildings.shp" % (self.output_dir, os.sep, self.extract_name)
        self.ds_buildings = self.building_driver.CreateDataSource(building_file)
        self.building_layer = self.ds_buildings.CreateLayer('building', spatialReference, ogr.wkbPolygon)
        self.building_def = self.building_layer.GetLayerDefn()

        self.square_driver = ogr.GetDriverByName("ESRI Shapefile")
        square_file = "%s%s%s_squares.shp" % (self.output_dir, os.sep, self.extract_name)
        self.ds_squares = self.square_driver.CreateDataSource(square_file)
        self.square_layer = self.ds_squares.CreateLayer('square', spatialReference, ogr.wkbPolygon)
        self.square_def = self.square_layer.GetLayerDefn()

        self.park_driver = ogr.GetDriverByName("ESRI Shapefile")
        park_file = "%s%s%s_parks.shp" % (self.output_dir, os.sep, self.extract_name)
        self.ds_parks = self.park_driver.CreateDataSource(park_file)
        self.park_layer = self.ds_parks.CreateLayer('park', spatialReference, ogr.wkbPolygon)
        self.park_def = self.park_layer.GetLayerDefn()

        self.wall_driver = ogr.GetDriverByName("ESRI Shapefile")
        wall_file = "%s%s%s_walls.shp" % (self.output_dir, os.sep, self.extract_name)
        self.ds_walls = self.wall_driver.CreateDataSource(wall_file)
        self.wall_layer = self.ds_walls.CreateLayer('wall', spatialReference, ogr.wkbLineString)
        if self.wall_layer.CreateField ( self.width_field ) != 0:
            print "Creating mat_id field failed.\n"
            return False
        self.wall_def = self.wall_layer.GetLayerDefn()

        self.tower_driver = ogr.GetDriverByName("ESRI Shapefile")
        tower_file = "%s%s%s_towers.shp" % (self.output_dir, os.sep, self.extract_name)
        self.ds_towers = self.tower_driver.CreateDataSource(tower_file)
        self.tower_layer = self.ds_towers.CreateLayer('tower', spatialReference, ogr.wkbPolygon)
        if self.tower_layer.CreateField ( self.visible_field ) != 0:
            print "Creating mat_id field failed.\n"
            return False
        self.tower_def = self.tower_layer.GetLayerDefn()

        self.tree_driver = ogr.GetDriverByName("ESRI Shapefile")
        tree_file = "%s%s%s_trees.shp" % (self.output_dir, os.sep, self.extract_name)
        self.ds_trees = self.tree_driver.CreateDataSource(tree_file)
        self.tree_layer = self.ds_trees.CreateLayer('tree', spatialReference, ogr.wkbPolygon)
        self.tree_def = self.tree_layer.GetLayerDefn()


        self.file = open(self.filepath)
        self.parse()


        self.file.close()

        self.ds_roads.Destroy()
        self.ds_rivers.Destroy()
        self.ds_lakes.Destroy()
        self.ds_buildings.Destroy()
        self.ds_squares.Destroy()
        self.ds_parks.Destroy()
        self.ds_walls.Destroy()
        self.ds_towers.Destroy()
        self.ds_trees.Destroy()

        return True

    def parse(self, ):
        self.file.readline()
        self.file.readline()
        self.file.readline()
        self.city_size = int(self.file.readline())
        for i in range(12) : self.file.readline()
        for i in range(4) : self.file.readline()
        self.line_object_number = int(self.file.readline())
        self.file.readline()
        self.file.readline()
        self.file.readline()

        if not self.parse_lines(): return False


        self.building_object_number = int(self.file.readline())
        print 'Buildings', self.line_object_number

        if not self.parse_buildings(): return False

        self.square_object_number = int(self.file.readline())
        print 'Squares', self.square_object_number
        self.file.readline()

        if not self.parse_squares(): return False

        self.file.readline()
        self.park_object_number = int(self.file.readline())
        print 'Parks', self.park_object_number
        self.file.readline()

        if not self.parse_parks(): return False

        has_walls = int(self.file.readline())
        print has_walls
        if has_walls > 0:
            self.wall_object_number = int(self.file.readline())
            self.wall_thickness = float(self.file.readline())
            if not self.parse_wall(): return False

            self.tower_object_number = int(self.file.readline())
            print 'Towers', self.tower_object_number

            if not self.parse_towers(): return False

        self.tree_object_number = int(self.file.readline())
        if not self.parse_trees(): return False

    def parse_lines(self, ):
        self.lake_poly = ogr.Geometry(ogr.wkbMultiPolygon)

        for i in range(self.line_object_number):
            line_type = int(self.file.readline())
            point_number = int(self.file.readline())
            line_width = float(self.file.readline())
            self.file.readline()
            lineString = []
            for y in range(point_number):
                posX = float(self.file.readline())
                posY = float(self.file.readline())*-1
                posPoint = (posX+self.position_correction['x'], posY+self.position_correction['y'])
                lineString.append(posPoint)


            if line_type == 0:
                if not self.add_road(lineString, line_width): return False
            elif line_type == 1:
                if not self.add_river(lineString, line_width): return False
            elif line_type == 2:
                if not self.add_lake(lineString): return False

            lineString = []

        #Saving the new lakes polygons
        lake_union = self.lake_poly.UnionCascaded()

        for i in range(lake_union.GetGeometryCount()):
            lake_feat = ogr.Feature( self.lake_def )
            lake_feat.SetGeometry(lake_union.GetGeometryRef(i))
            if self.lake_layer.CreateFeature(lake_feat) != 0:
                return False

            lake_feat.Destroy()

        return True

    def parse_buildings(self, ):
        for i in range(self.building_object_number):
            self.file.readline()
            building_type = int(self.file.readline())
            lineString = []
            if building_type == 0:
                for y in range(4):
                    posX = float(self.file.readline())
                    posY = float(self.file.readline())*-1
                    posPoint = (posX+self.position_correction['x'], posY+self.position_correction['y'])
                    lineString.append(posPoint)
                self.add_building(building_type, lineString)
            else:
                posX = float(self.file.readline())
                posY = float(self.file.readline())*-1
                width = float(self.file.readline())
                self.add_building(building_type, {'x':posX+self.position_correction['x'], 'y':posY+self.position_correction['y'], 'width':width})
            lineString = []

        return True

    def parse_squares(self, ):
        for i in range(self.square_object_number):
            print 'dump', self.file.readline()
            point_number = int(self.file.readline())
            print 'point_number', point_number
            if point_number > 0:
                self.file.readline()
                lineString = []
                for y in range(point_number):
                    posX = float(self.file.readline())
                    posY = float(self.file.readline())*-1
                    posPoint = (posX+self.position_correction['x'], posY+self.position_correction['y'])
                    lineString.append(posPoint)

                if len(lineString) > 0:
                    if not self.add_square(lineString): return False

                lineString = []

        return True

    def parse_parks(self, ):
        for i in range(self.park_object_number):
            print 'dump', self.file.readline()
            point_number = int(self.file.readline())
            print 'point_number', point_number
            if point_number > 0:
                self.file.readline()
                lineString = []
                for y in range(point_number):
                    posX = float(self.file.readline())
                    posY = float(self.file.readline())*-1
                    posPoint = (posX+self.position_correction['x'], posY+self.position_correction['y'])
                    lineString.append(posPoint)

                if len(lineString) > 0:
                    if not self.add_park(lineString): return False

                lineString = []

        return True

    def parse_wall(self, ):
        lineString = []
        for i in range(self.wall_object_number):
            posX = float(self.file.readline())
            posY = float(self.file.readline())*-1
            posPoint = (posX+self.position_correction['x'], posY+self.position_correction['y'])
            lineString.append(posPoint)

            connect = int(self.file.readline())

            if connect == 0:
                if not self.add_wall(lineString): return False

                lineString = []

        if not self.add_wall(lineString): return False

        return True

    def parse_towers(self, ):
        for i in range(self.tower_object_number):
            tower_visibility = int(self.file.readline())
            tower_type = int(self.file.readline())
            lineString = []
            if tower_type == 2:
                for y in range(4):
                    posX = float(self.file.readline())
                    posY = float(self.file.readline())*-1
                    posPoint = (posX+self.position_correction['x'], posY+self.position_correction['y'])
                    lineString.append(posPoint)
                self.add_tower(tower_type, lineString, tower_visibility)
            else:
                posX = float(self.file.readline())
                posY = float(self.file.readline())*-1
                width = float(self.file.readline())
                self.add_tower(tower_type, {'x':posX+self.position_correction['x'], 'y':posY+self.position_correction['y'], 'width':width}, tower_visibility)
            lineString = []

        return True

    def parse_trees(self, ):
        for i in range(self.tree_object_number):
            posX = float(self.file.readline())
            posY = float(self.file.readline())*-1
            size = float(self.file.readline())
            posPoint = (posX+self.position_correction['x'], posY+self.position_correction['y'])
            if not self.add_tree(posPoint, size): return False


        return True

    def add_road(self, lineString, width):
        road_feat = ogr.Feature( self.road_def )
        road_feat.SetField( "width", width )
        road_line = ogr.Geometry(ogr.wkbLineString)
        for point in lineString:
            road_line.AddPoint(point[0], point[1])

        road_feat.SetGeometry(road_line)
        if self.road_layer.CreateFeature(road_feat) != 0:
            sys.exit( 1 )

        road_feat.Destroy()
        return True

    def add_river(self, lineString, width):
        river_feat = ogr.Feature( self.river_def )
        river_feat.SetField( "width", width )
        river_line = ogr.Geometry(ogr.wkbLineString)
        for point in lineString:
            river_line.AddPoint(point[0], point[1])

        river_feat.SetGeometry(river_line)
        if self.river_layer.CreateFeature(river_feat) != 0:
            sys.exit( 1 )

        river_feat.Destroy()
        return True

    def add_lake(self, lineString):
        lake_point = ogr.Geometry(type=ogr.wkbPoint)
        for point in lineString:
            lake_point.SetPoint(0, point[0], point[1])
            self.lake_poly.AddGeometry(lake_point.Buffer(5, 30))

        return True

    def add_building(self, building_type, building_object):
        building_feat = ogr.Feature( self.building_def )
        building_poly = ogr.Geometry(ogr.wkbPolygon)
        if building_type == 0:
            building_line = ogr.Geometry(ogr.wkbLinearRing)
            for point in building_object:
                building_line.AddPoint(point[0], point[1])

            building_line.AddPoint(building_object[0][0], building_object[0][1])
            building_poly.AddGeometry(building_line)
        else:
            building_point = ogr.Geometry(type=ogr.wkbPoint)
            building_point.SetPoint(0, building_object['x'], building_object['y'])
            building_poly = building_point.Buffer(building_object['width'], 30)

        building_feat.SetGeometry(building_poly)
        if self.building_layer.CreateFeature(building_feat) != 0:
            return False

        building_feat.Destroy()
        return True

    def add_square(self, lineString):
        square_feat = ogr.Feature( self.square_def )
        square_poly = ogr.Geometry(ogr.wkbPolygon)

        square_line = ogr.Geometry(ogr.wkbLinearRing)
        for point in lineString:
            square_line.AddPoint(point[0], point[1])

        square_line.AddPoint(lineString[0][0], lineString[0][1])
        square_poly.AddGeometry(square_line)

        square_feat.SetGeometry(square_poly)
        if self.square_layer.CreateFeature(square_feat) != 0:
            return False

        square_feat.Destroy()
        return True

    def add_park(self, lineString):
        park_feat = ogr.Feature( self.park_def )
        park_poly = ogr.Geometry(ogr.wkbPolygon)

        park_line = ogr.Geometry(ogr.wkbLinearRing)
        for point in lineString:
            park_line.AddPoint(point[0], point[1])

        park_line.AddPoint(lineString[0][0], lineString[0][1])
        park_poly.AddGeometry(park_line)

        park_feat.SetGeometry(park_poly)
        if self.park_layer.CreateFeature(park_feat) != 0:
            return False

        park_feat.Destroy()
        return True

    def add_wall(self, lineString):
        wall_feat = ogr.Feature( self.wall_def )
        wall_feat.SetField( "width", self.wall_thickness )
        wall_line = ogr.Geometry(ogr.wkbLineString)
        for point in lineString:
            wall_line.AddPoint(point[0], point[1])

        wall_feat.SetGeometry(wall_line)
        if self.wall_layer.CreateFeature(wall_feat) != 0:
            sys.exit( 1 )

        wall_feat.Destroy()
        return True

    def add_tower(self, tower_type, tower_object, visibility):
        tower_feat = ogr.Feature( self.tower_def )
        tower_feat.SetField( "visible", visibility )
        tower_poly = ogr.Geometry(ogr.wkbPolygon)
        if tower_type == 2:
            tower_line = ogr.Geometry(ogr.wkbLinearRing)
            for point in tower_object:
                tower_line.AddPoint(point[0], point[1])

            tower_line.AddPoint(tower_object[0][0], tower_object[0][1])
            tower_poly.AddGeometry(tower_line)
        else:
            tower_point = ogr.Geometry(type=ogr.wkbPoint)
            tower_point.SetPoint(0, tower_object['x'], tower_object['y'])
            tower_poly = tower_point.Buffer(tower_object['width'], 30)

        tower_feat.SetGeometry(tower_poly)
        if self.tower_layer.CreateFeature(tower_feat) != 0:
            return False

        tower_feat.Destroy()
        return True

    def add_tree(self, point, size):
        tree_feat = ogr.Feature( self.tree_def )
        tree_poly = ogr.Geometry(ogr.wkbPolygon)


        tree_point = ogr.Geometry(ogr.wkbPoint)
        tree_point.SetPoint(0, point[0], point[1])

        tree_poly = tree_point.Buffer(size, 30)

        tree_feat.SetGeometry(tree_poly)
        if self.tree_layer.CreateFeature(tree_feat) != 0:
            sys.exit( 1 )

        tree_feat.Destroy()
        return True
