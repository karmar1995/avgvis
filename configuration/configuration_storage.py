from model.composition_root import MapData

import json


class ConfigurationInJson:
    def __init__(self):
        super().__init__()
        self.data = None

    def read(self, filename):
        with open(filename, 'r') as f:
            self.data = json.load(f)

    def hasMapData(self):
        try:
            tmp = self.data['mapData']
            return True
        except KeyError:
            return False

    def saveMapData(self, mapData):
        pass

    def mapData(self):
        node = self.data['mapData']
        mapData = MapData(x=node['x'], y=node['y'], width=node['width'], height=node['height'])
        return mapData

    def objectsList(self):
        objectsList = list()
        objects = self.data['objects']
        for object in objects:
            registerData = dict()
            registerData['name'] = object['name']
            registerData['sourceType'] = object['sourceType']
            registerData['width'] = float(object['width'])
            registerData['height'] = float(object['height'])
            registerData['type'] = object['type']
            registerData['connectionString'] = object['connectionString']
            registerData['xSignal'] = object['xSignal'].split('/')
            registerData['ySignal'] = object['ySignal'].split('/')
            registerData['rotationSignal'] = object['rotationSignal'].split('/')
            registerData['updateInterval'] = float(object['updateInterval'])
            registerData['properties'] = dict()
            for propertyNode in object['properties']:
                registerData['properties'][propertyNode] = object['properties'][propertyNode].split('/')
            registerData['alerts'] = dict()
            for alertNode in object['alerts']:
                registerData['alerts'][alertNode] = object['alerts'][alertNode].split('/')

            objectsList.append(registerData)
        return objectsList
