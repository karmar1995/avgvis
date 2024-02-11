import json
from mes_adapter.request_parser import *


class JsonRequestParser(RequestParser):
    def parse(self, data) -> MesRequest:
        parsed = json.loads(data)
        return MesRequest(orderId=parsed['productionOrderId'])