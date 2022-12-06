from utils import spot
spot.init()

config = {
	"okay": [spot.stand, {}],
	"peace": [spot.lay, {}],
	"thumbs up": [spot.sit, {"param2" : 555}],
	"thumbs down": [None, {}],
	"call me": [None, {}],
	"stop": [None, {}],
	"rock": [None, {}],
	"live long": [spot.twerk, {"interval":.5, "duration":8}],
	"fist": [spot.twerk, {"duration": 15}],
	"smile": [None, {}],
}