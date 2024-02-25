import json
from mes_adapter.request_parser import *


class JsonRequestParser(RequestParser):
    def parse(self, data) -> MesRequest:
        try:
            parsed = json.loads(data)
            return MesRequest(orderId=parsed['productionOrderId'])
        except Exception:
            return MesRequest(orderId=-1)