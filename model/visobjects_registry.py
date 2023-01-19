class VisObjectsRegistry:
    def __init__(self):
        self.visObjectsById = {}

    def registerObject(self, visObject):
        self.visObjectsById[visObject.id] = visObject

    def unregisterObject(self, visObjectId):
        del self.visObjectsById[visObjectId]

