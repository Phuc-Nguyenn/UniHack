extends Node2D

# Called when the node enters the scene tree for the first time.
func _ready():
	var server = HttpServer.new()
	server.register_router("/start_ducking", MyExampleRouter.new())
	add_child(server)
	server.start()
