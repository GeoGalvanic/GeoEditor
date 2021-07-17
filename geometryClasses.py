'''
This file is responsible for creating classes that represent each object within a geodataframe.
'''
import matplotlib.patches as ptch

class Entity():
    '''Abstract base class for entities. Shold not be called directly, insead sub-classes should be used.'''
    def __init__(self,gdfRow,layer, displayField = 0):
        self.gdfRow = gdfRow
        self.layer = layer
        self.displayField = displayField

        self.patches = []

        self.createPatches()

    def createPatches(self):
        '''Function that creates matplotlib patch objects given the gdfRows current geometry.'''
        pass

    def pickAction(self, mouse, blind):
        print(self.gdfRow)

    def __str__(self):
        return str(self.gdfRow[self.displayField])

class PolygonEntity(Entity):
    def __init__(self,gdfRow,layer):
        super(PolygonEntity,self).__init__(gdfRow,layer)
    
    def createPatches(self):
        poly = self.gdfRow.geometry
        coordSequence = poly.exterior.coords
        coordList = []
        for coord in coordSequence:
            coordList.append(coord)

        self.patches.append(ptch.Polygon(coordList, color = self.layer.color, picker=True))

