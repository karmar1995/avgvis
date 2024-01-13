from dataclasses import dataclass


@dataclass
class AgvStatus:
    online: bool
    location: str


def agvStatusFromJson(statusString):
    raise NotImplementedError()

def agvIdsFromJson(idsString):
    raise NotImplementedError()