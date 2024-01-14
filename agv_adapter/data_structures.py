from dataclasses import dataclass
import json


@dataclass
class AgvStatus:
    agvId: str
    online: bool
    location: str


def agvStatusFromJson(statusString):
    if statusString != "":
        response = json.loads(statusString)
        return AgvStatus(str(response['agvId']), response['online'], str(response['location']))
    return AgvStatus("", False, "0")


def agvIdsFromJson(idsString):
    if idsString != "":
        return json.loads(idsString)['agvs']
    return []