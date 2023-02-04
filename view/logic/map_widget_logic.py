from collections import namedtuple
from model.model_view import AbstractModelView

Point = namedtuple('Point', 'x y')


class VisualizationWidgetLogic:
    def __init__(self, selection):
        self.__x = None
        self.__y = None
        self.__width = None
        self.__height = None
        self.__properties = None
        self.__selection = selection
        self.__objectObserver = None
        self.__modelX = None
        self.__modelY = None

    def initialize(self, x, y, width, height, properties):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__properties = properties

    def setObserver(self, observer):
        self.__objectObserver = observer

    def setPosition(self, x, y):
        self.__x = x
        self.__y = y
        self.__broadcastObjectChanged()

    def setModelPosition(self, x, y):
        self.__modelX = x
        self.__modelY = y

    def getBoundingRect(self):
        top_left_x = self.__x - int(self.__width / 2)
        top_left_y = self.__y - int(self.__height / 2)
        return int(top_left_x), int(top_left_y), int(self.__width), int(self.__height)

    def getShapePoints(self):
        points = list()
        shape_width = self.__width / 4
        shape_height = self.__height / 4
        origin_x = self.__x
        origin_y = self.__y - shape_height / 2
        points.append(Point(int(origin_x), int(origin_y)))
        points.append(Point(int(origin_x + shape_width / 2), int(origin_y + shape_height)))
        points.append(Point(int(origin_x - shape_width / 2), int(origin_y + shape_height)))
        return points

    def properties(self):
        properties_dict = dict()
        properties_dict['x'] = str(self.__modelX)
        properties_dict['y'] = str(self.__modelY)
        return { **self.__properties, **properties_dict }

    def updateSelection(self):
        self.__selection.updateSelection(self)

    def isSelected(self):
        return self.__selection.selectedObject() == self

    def __broadcastObjectChanged(self):
        if self.__objectObserver:
            self.__objectObserver.objectChanged()


class MapWidgetLogic:
    def __init__(self, viewAccess, selection):
        self.modelMap = None
        self.viewAccess = viewAccess
        self.objectsDict = {}
        self.xScaling = 1.0
        self.yScaling = 1.0
        self.mapOrigin = 0, 0
        self.rowHeight = 10
        self.columnWidth = 10
        self.selection = selection

    def updateObject(self, visobject):
        if visobject.getObjectId() not in self.objectsDict:
            self.registerObject(visobject)

        objectToUpdate = self.objectsDict[visobject.getObjectId()]
        x = self.offsetX(visobject.getX())
        y = self.offsetY(visobject.getY())
        objectToUpdate.setPosition(x, y)
        objectToUpdate.setModelPosition(visobject.getX(), visobject.getY())
        self.viewAccess.updateView()

    def registerObject(self, visobject):
        self.objectsDict[visobject.getObjectId()] = \
            VisualizationWidgetLogic(self.selection)
        self.objectsDict[visobject.getObjectId()].initialize(
            x=self.offsetX(visobject.getX()),
            y=self.offsetY(visobject.getY()),
            width=visobject.getWidth() * self.xScaling,
            height=visobject.getHeight() * self.yScaling,
            properties=visobject.getProperties()
        )
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
        self.xScaling = viewSize.width() / modelSize[1]
        self.yScaling = viewSize.height() / modelSize[0]

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
