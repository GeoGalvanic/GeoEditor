'''
This file is responsible for creating classes that represent each object within a geodataframe.
'''
import matplotlib.patches as ptch
from shapely.geometry import MultiPolygon, MultiPoint, MultiLineString
from matplotlib.lines import Line2D

class Entity():
    '''Abstract base class for entities. Shold not be called directly, insead sub-classes should be used.'''
    def __init__(self,gdfRow,layer):
        self.gdfRow = gdfRow
        self.layer = layer

        self.patches = []
        self.artists = []

        self.createPatches()

    def createPatches(self):
        '''Function that creates matplotlib patch objects given the gdfRows current geometry.'''
        pass

    def pickAction(self, mouse, blind):
        print(self.gdfRow)

    def __str__(self):
        return f"{self.gdfRow[self.layer.displayField]} : {self.layer.name}"

class PolygonEntity(Entity):
    def __init__(self,gdfRow,layer):
        super(PolygonEntity,self).__init__(gdfRow,layer)
    
    def createPatches(self):
        geom = self.gdfRow.geometry

        for poly in geom if type(geom) == MultiPolygon else [geom]:
            coordSequence = poly.exterior.coords
            coordList = []
            for coord in coordSequence:
                coordList.append(coord)

            self.patches.append(ptch.Polygon(coordList, facecolor = self.layer.color, edgecolor = "black", picker=-10))

class PointEntity(Entity):
    def __init__(self,gdfRow,layer):
        super(PointEntity,self).__init__(gdfRow,layer)
    
    def createPatches(self):
        geom = self.gdfRow.geometry

        for point in geom if type(geom) == MultiPoint else [geom]:
            self.artists.append(Line2D([point.x],[point.y], marker="o", markerfacecolor="b", markersize=7, picker=30))

class LineEntity(Entity):
    def __init__(self,gdfRow,layer):
        super(LineEntity,self).__init__(gdfRow,layer)
    
    def createPatches(self):
        geom = self.gdfRow.geometry

        for line in geom if type(geom) == MultiLineString else [geom]:
            self.artists.append(Line2D([point[0] for point in line.coords],[point[1] for point in line.coords], lw = 2, color = "green", picker=30))