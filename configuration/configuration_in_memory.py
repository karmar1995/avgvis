from model.composition_root import MapData

import json


class ConfigurationInMemory:
    def __init__(self):
        pass

    def hasMapData(self):
        return False

    def mapData(self):
        return None

    def saveMapData(self, mapData):
        pass


class ConfigurationInJson(ConfigurationInMemory):

    def __init__(self):
        super().__init__()
        self.filename = "config.json"
        self.data = None
        with open(self.filename, 'r') as f:
            self.data = json.load(f)

    def hasMapData(self):
        try:
            tmp = self.data['mapData']
            return True
        except KeyError:
            return False

    def mapData(self):
        node = self.data['mapData']
        mapData = MapData(x=node['x'], y=node['y'], width=node['width'], height=node['height'])
        return mapData

    def objectsList(self):
        objectsList = list()
        objects = self.data['objects']
        for object in objects:
            registerData = dict()
            registerData['sourceType'] = object['sourceType']
            registerData['width'] = float(object['width'])
            registerData['height'] = float(object['height'])
            registerData['type'] = object['type']
            registerData['connectionString'] = object['connectionString']
            registerData['xSignal'] = object['xSignal'].split('/')
            registerData['ySignal'] = object['ySignal'].split('/')
            registerData['updateInterval'] = float(object['updateInterval'])
            objectsList.append(registerData)
        return objectsList
