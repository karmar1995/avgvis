from dataclasses import dataclass


@dataclass
class MesRequest:
    orderId: int


class RequestParser:
    def parse(self, data) -> MesRequest:
        raise NotImplementedError()