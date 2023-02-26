from model.composition_root import MapData
from os.path import exists
import json


class ConfigurationInJson:
    def __init__(self):
        super().__init__()
        self.__data = None
        self.__filename = ""

    def fileExists(self, filename):
        return exists(filename)

    def setFilename(self, filename):
        self.__filename = filename

    def read(self, filename):
        with open(filename, 'r') as f:
            self.__data = json.load(f)

    def hasMapData(self):
        try:
            tmp = self.__data['mapData']
            return True
        except KeyError:
            return False

    def saveMapData(self, mapData):
        pass

    def mapData(self):
        node = self.__data['mapData']
        mapData = MapData(x=node['x'], y=node['y'], width=node['width'], height=node['height'])
        return mapData

    def objectsList(self):
        objectsList = list()
        objects = self.__data['objects']
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
