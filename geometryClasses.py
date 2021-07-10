'''
This file is responsible for creating classes that represent each object within a geodataframe.
'''

import geopandas as gpd
import matplotlib.patches as ptch
from numpy import array

class Entity():
    def __init__(self,gdfRow):
        self.gdfRow = gdfRow
        self.patches = []

        self.createPatches()

    def createPatches(self):
        pass

    def pickAction(self, mouse, blind):
        print(self.gdfRow)

class PolygonEntity(Entity):
    def __init__(self,gdfRow):
        super(PolygonEntity,self).__init__(gdfRow)
    
    def createPatches(self):
        poly = self.gdfRow.geometry
        coordSequence = poly.exterior.coords
        coordList = []
        for coord in coordSequence:
            coordList.append(coord)

        self.patches.append(ptch.Polygon(coordList, color="blue", picker=True))
