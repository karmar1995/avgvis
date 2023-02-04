from collections import namedtuple
from model.model_view import AbstractModelView

Point = namedtuple('Point', 'x y')


class VisualizationWidgetLogic:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getBoundingRect(self):
        top_left_x = self.x - int(self.width / 2)
        top_left_y = self.y - int(self.height / 2)
        return int(top_left_x), int(top_left_y), int(self.width), int(self.height)

    def getShapePoints(self):
        points = list()
        shape_width = self.width / 4
        shape_height = self.height / 4
        origin_x = self.x
        origin_y = self.y - shape_height / 2
        points.append(Point(int(origin_x), int(origin_y)))
        points.append(Point(int(origin_x + shape_width / 2), int(origin_y + shape_height)))
        points.append(Point(int(origin_x - shape_width / 2), int(origin_y + shape_height)))
        return points


class MapWidgetLogic:
    def __init__(self, viewAccess):
        self.modelMap = None
        self.viewAccess = viewAccess
        self.objectsDict = {}
        self.xScaling = 1.0
        self.yScaling = 1.0
        self.mapOrigin = 0, 0
        self.rowHeight = 10
        self.columnWidth = 10

    def updateObject(self, visobject):
        if visobject.getObjectId() not in self.objectsDict:
            self.registerObject(visobject)

        objectToUpdate = self.objectsDict[visobject.getObjectId()]
        x = self.offsetX(visobject.getX())
        y = self.offsetY(visobject.getY())
        objectToUpdate.setPosition(x, y)
        self.viewAccess.updateView()

    def registerObject(self, visobject):
        self.objectsDict[visobject.getObjectId()] = \
            VisualizationWidgetLogic(self.offsetX(visobject.getX()), self.offsetY(visobject.getY()),
                                     visobject.getWidth() * self.xScaling, visobject.getHeight() * self.yScaling)
        self.viewAccess.addObject(self.objectsDict[visobject.getObjectId()])

    def unregisterObject(self, visobjectId):
        try:
            del self.objectsDict[visobjectId]
            self.viewAccess.eraseObject(visobjectId)
            self.viewAccess.updateView()
        except KeyError:
            pass

    def renderMap(self, modelMap):
        self.modelMap = modelMap
        self.updateScaling()
        self.updateOrigin()
        self.viewAccess.updateGrid(self.columnWidth * self.xScaling, self.rowHeight * self.yScaling)
        self.viewAccess.showMap()

    def updateScaling(self):
        viewSize = self.viewAccess.size()
        modelSize = self.modelMap.size()
        self.xScaling = viewSize.width() / modelSize[0]
        self.yScaling = viewSize.height() / modelSize[1]

    def updateOrigin(self):
        self.mapOrigin = self.modelMap.x(), self.modelMap.y()

    def offsetX(self, x):
        modelDistance = x - self.mapOrigin[0]
        return modelDistance * self.xScaling

    def offsetY(self, y):
        modelDistance = y - self.mapOrigin[1]
        return modelDistance * self.yScaling


class ModelViewToMapLogicAdapter(AbstractModelView):
    def __init__(self, mapLogic: MapWidgetLogic):
        super().__init__()
        self.mapLogic = mapLogic

    def renderObject(self, visObject):
        self.mapLogic.updateObject(visObject)

    def cleanupObject(self, visObjectId):
        self.mapLogic.unregisterObject(visObjectId)

    def showCollision(self, collidingObjects):
        pass

    def renderMap(self, visMap):
        self.mapLogic.renderMap(visMap)
