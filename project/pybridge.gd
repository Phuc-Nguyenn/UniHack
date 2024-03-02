extends Node

var DIR = OS.get_executable_path().get_base_dir()
var BIN_PATH = DIR.plus_file("bin/main/main")

func _ready():
	# Run the process in the background, while the game is running
	OS.create_process(BIN_PATH, [])
