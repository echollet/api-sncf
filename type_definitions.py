#
#
#

# https://docs.python.org/3.8/library/typing.html

from collections import namedtuple
from typing import List


Route = namedtuple("Route", ["id","name","line"])
Routes = List[Route]

Line = namedtuple("Line", ["id", "name", "code", "network"])
Lines = List[Line]

StopArea = namedtuple("StopArea", ["id", "name", "label"])
StopAreas = List[StopArea]

StopPoint = namedtuple("StopPoint", ["id", "name", "label", "type"])
StopPoints = List[StopPoint]

Network = namedtuple("Network", ["id", "name"])
Networks = List[Network]