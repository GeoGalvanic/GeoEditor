'''
This file contains the layer and layer manager classes which store features and contain other data.
'''
import os
import geopandas as gpd
import geometryClasses
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, Point, MultiPoint

class Layer():
    activeLayers = []
    '''Layer describes the GeoDataframe, Entity Objects and Plotted Artists for a given source file within a given axis.'''
    def __init__(self, source, axis, displayField = 0, layerName = None):
        self.source = source
        self.gdf = gpd.read_file(source)
        self.axis = axis

        self.entities = []
        self.artistEntityPairs = {}

        self.color = "red"
        self.displayField = displayField
        self.selectable = True #Determines wheter artists of this layer will have pick events

        self._generateEntities()
        self.drawArtists()

        self.name = os.path.basename(self.source).split('.')[0] if layerName == None else layerName

        Layer.activeLayers.append(self)

    def __str__(self):
        return self.name

    def _generateEntities(self):
        for i, row in self.gdf.iterrows():
            geomType = type(row.geometry)
            if geomType == Polygon or geomType == MultiPolygon:
                entity = geometryClasses.PolygonEntity(row,self)
            elif geomType == Point or geomType == MultiPoint:
                entity = geometryClasses.PointEntity(row,self)
            elif geomType == LineString or geomType == MultiLineString:
                entity = geometryClasses.LineEntity(row,self)
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

    def changeName(self, value):
        self.name = value
    
    def saveSource(self):
        pass

    def saveToFile(self):
        pass

    def discardEdits(self):
        pass

    def saveLayerAsFile(self):
        pass

    def setSelectable(self,value):
        self.selectable = value

        if value == True:
            for artist in self.artistEntityPairs:
                if type(self.artistEntityPairs[artist]) == geometryClasses.PolygonEntity:
                    artist.set_picker(-10)
                else:
                    artist.set_picker(30)
        else:
            for artist in self.artistEntityPairs:
                artist.set_picker(None)

