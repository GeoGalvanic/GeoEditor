'''
This file contains the layer and layer manager classes which store features and contain other data.
'''
import geopandas as gpd
import geometryClasses
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, Point, MultiPoint

class Layer():
    '''Layer describes the GeoDataframe, Entity Objects and Plotted Artists for a given source file within a given axis.'''
    def __init__(self, source, axis):
        self.source = source
        self.gdf = gpd.read_file(source)
        self.axis = axis

        self.entities = []
        self.artistEntityPairs = {}

        self.color = "red"

        self._generateEntities()
        self.drawArtists()

    def _generateEntities(self):
        for i, row in self.gdf.iterrows():
            geomType = type(row.geometry)
            if geomType == type(Polygon) or type(MultiPolygon):
                entity = geometryClasses.PolygonEntity(row,self)
            self.entities.append(entity)

    def drawArtists(self):
        self.artists = []
        for entity in self.entities:
            for patch in entity.patches:
                artist = self.axis.add_patch(patch)
                self.artistEntityPairs[artist] = entity
        return True
