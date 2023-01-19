class Map:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def topLeft(self):
        return self.x, self.y

    def bottomRight(self):
        return self.x + self.width, self.y + self.height

