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
        try:
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

            self.displayField = displayField
            self.selectable = True #Determines wheter artists of this layer will have pick events

            self._generateEntities()
            self.drawArtists()

            self.name = os.path.basename(self.source).split('.')[0] if layerName == None else layerName

            Layer.activeLayers.append(self)
        except:
            dialogGUI.ErrorDialog(f'Initializing Layer. Source: {source}, Axis: {axis}, Display: {displayField}, Name: {layerName}')
    
    def __str__(self):
        return self.name

    def _generateEntities(self):
        try:
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
        except:
            dialogGUI.ErrorDialog(f'generating entities for {self}')

    def drawArtists(self):
        try:
            for entity in self.entities:
                for patch in entity.patches:
                    artist = self.axis.add_patch(patch)
                    self.artistEntityPairs[artist] = entity
                for artist in entity.artists:
                    self.axis.add_artist(artist)
                    self.artistEntityPairs[artist] = entity
            return True
        
        except:
            dialogGUI.ErrorDialog(f'Drawing artists for {self}')

            return False

    def changeName(self, value):
        self.name = value
    
    def saveData(self, file = None):
        file = file if file else self.source

        try:
            self.gdf.to_file(file)
        except:
            dialogGUI.ErrorDialog(f'Exporting {self} to {file}')

    def saveLayerAsFile(self):
        pass

    def setSelectable(self,value):
        self.selectable = value

        if value == True:
            try:
                for artist in self.artistEntityPairs:
                    if type(self.artistEntityPairs[artist]) == geometryClasses.PolygonEntity:
                        artist.set_picker(-10)
                    else:
                        artist.set_picker(30)
            except:
                dialogGUI.ErrorDialog(f'Creating pick events for artists in {self}')

        else:
            try:
                for artist in self.artistEntityPairs:
                    artist.set_picker(None)
            except:
                dialogGUI.ErrorDialog(f'Removing pick events for {self}')

    def redrawArtists(self):
        try:
            for artist in self.artistEntityPairs:
                if type(self.artistEntityPairs[artist]) == geometryClasses.PolygonEntity:
                    artist.set(**self.polygonSymbology)

                if type(self.artistEntityPairs[artist]) == geometryClasses.LineEntity:
                    artist.set(**self.lineSymbology)

                if type(self.artistEntityPairs[artist]) == geometryClasses.PointEntity:
                    artist.set(**self.pointSymbology)

                mplElements.GEFigure.figures[-1].draw_artist(artist)
            
            mplElements.GEFigure.figures[-1].canvas.draw()
        except:
            dialogGUI.ErrorDialog(f'Redrawing artists in {self}')

    def removeSelf(self):
        try:
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
        
        except:
            dialogGUI.ErrorDialog(f'Removing layer {self}')

