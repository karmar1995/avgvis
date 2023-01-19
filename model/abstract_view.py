class AbstractView:
    def __init__(self):
        pass

    def renderObject(self, visObject):
        raise "Not implemented!"

    def showCollision(self, collidingObjects):
        raise "Not implemented!"

    def renderMap(self, visMap):
        raise "Not implemented!"

