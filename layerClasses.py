'''
This file contains the layer and layer manager classes which store features and contain other data.
'''
import geopandas as gpd
import geometryClasses
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, Point, MultiPoint

class Layer():
    activeLayers = []
    '''Layer describes the GeoDataframe, Entity Objects and Plotted Artists for a given source file within a given axis.'''
    def __init__(self, source, axis, displayField = 0):
        self.source = source
        self.gdf = gpd.read_file(source)
        self.axis = axis

        self.entities = []
        self.artistEntityPairs = {}

        self.color = "red"
        self.displayField = displayField

        self._generateEntities()
        self.drawArtists()

        Layer.activeLayers.append(self)

    def _generateEntities(self):
        for i, row in self.gdf.iterrows():
            geomType = type(row.geometry)
            if geomType == Polygon or geomType == MultiPolygon:
                entity = geometryClasses.PolygonEntity(row,self,self.displayField)
            elif geomType == Point or geomType == MultiPoint:
                entity = geometryClasses.PointEntity(row,self,self.displayField)
            elif geomType == LineString or geomType == MultiLineString:
                entity = geometryClasses.LineEntity(row,self,self.displayField)
            else:
                print('invalid geometry type')
            self.entities.append(entity)

    def drawArtists(self):
        for entity in self.entities:
            for patch in entity.patches:
                artist = self.axis.add_patch(patch)
                self.artistEntityPairs[artist] = entity
            for artist in entity.artists:
                self.axis.add_artist(artist)
                self.artistEntityPairs[artist] = entity
        return True
