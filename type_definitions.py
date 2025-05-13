#
#
#

from collections import namedtuple

StopPoint = namedtuple("StopPoint", "id name label")
StopPoints = namedtuple("StopPoints", "train_stops long_dist_train_stops")