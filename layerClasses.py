'''
This file contains the layer and layer manager classes which store features and contain other data.
'''
import os
import geopandas as gpd
import geometryClasses
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, Point, MultiPoint
import dialogGUI
import mplElements

class Layer():
    activeLayers = []
    '''Layer describes the GeoDataframe, Entity Objects and Plotted Artists for a given source file within a given axis.'''
    def __init__(self, source, axis, displayField = 0, layerName = None):
        self.source = source
        self.gdf = gpd.read_file(source)
        self.axis = axis

        self.entities = []
        self.artistEntityPairs = {}

        self.pointSymbology = {
            'marker' : 'o',
            'markeredgecolor' : 'gray',
            'markeredgewidth' : 0.7,
            'markerfacecolor' : 'blue',
            'markersize' : 8
        }

        self.lineSymbology = {
            'color' : 'green',
            'linestyle' : '-',
            'linewidth' : 2
        }

        self.polygonSymbology = {
            'facecolor' : 'red',
            'edgecolor' : 'gray',
            'linestyle' : '-',
            'linewidth' : 1,
            'joinstyle' : 'round'
        }

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
                entity = geometryClasses.PolygonEntity(i,self)
            elif geomType == Point or geomType == MultiPoint:
                entity = geometryClasses.PointEntity(i,self)
            elif geomType == LineString or geomType == MultiLineString:
                entity = geometryClasses.LineEntity(i,self)
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
    
    def saveData(self, file = None):
        file = file if file else self.source

        self.gdf.to_file(file)

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

    def removeSelf(self):
        for artist in self.artistEntityPairs:
            artist.remove()
            del artist
        self.artistEntityPairs = {}


        curAttWindow = dialogGUI.AttributeDialog.existingWindow
        if curAttWindow:
            entitiesToRemove = []
            for entity in curAttWindow.entities:
                if entity.layer == self:
                    entitiesToRemove.append(entity)

            while entitiesToRemove:
                entity = entitiesToRemove.pop()
                curAttWindow.removeEntity(entity)

        while self.entities:
            entity = self.entities.pop()
            del entity

        Layer.activeLayers.remove(self)

        mplElements.GEFigure.figures[-1].canvas.draw()

