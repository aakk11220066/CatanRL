class InsufficientResourcesException(Exception):
    pass


class InvalidPlacementException(Exception):
    pass


class InvalidSettlementPlacementException(InvalidPlacementException):
    pass


class InvalidCityPlacementException(InvalidPlacementException):
    pass


class InvalidRoadPlacementException(InvalidPlacementException):
    pass

class InvalidActionException(Exception):
    pass