from utils import spot
from typing import Any, Callable


config: dict[str, tuple[Callable[...], dict[str, Any]]] = {
	"okay"        : [spot.stand, {}],
	"peace"       : [spot.sit, {}],
	"thumbs up"   : [spot.lay, {}],
	"thumbs down" : [spot.twerk, {}],
	"call me"     : [None, {}],
	"stop"        : [None, {}],
	"rock"        : [spot.turnOn, {}],
	"live long"   : [spot.twerk, {"interval" : .2, "duration":5}],
	"fist"        : [spot.turnOff, {}],
	"smile"       : [None, {}],
}