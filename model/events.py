from collections import namedtuple

RegisterObjectEvent = namedtuple("RegisterObjectEvent", 'objectId type properties width height')
UpdateObjectPositionEvent = namedtuple("UpdateObjectPositionEvent", 'objectId x y')
UpdateObjectRotationEvent = namedtuple("UpdateObjectRotationEvent", 'objectId rotation')
UpdateObjectPropertiesEvent = namedtuple("UpdateObjectPropertiesEvent", 'objectId properties')
UnregisterObjectEvent = namedtuple("UnregisterObjectEvent", 'objectId')
