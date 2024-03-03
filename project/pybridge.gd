extends Node

var DIR = OS.get_executable_path().get_base_dir()
var BIN_PATH = DIR.plus_file("bin/main/main")

const UDP_IP := "127.0.0.1"
const UDP_PORT := 50505

var server := UDPServer.new()
var process_pids := []

func _ready():
	# Run the process in the background, while the game is running
	OS.create_process(BIN_PATH, [])
	server_start()


func _process(_delta):
	server.poll()
	if server.is_connection_available():
		var peer := server.take_connection()
		var packet = peer.get_packet().get_string_from_utf8()
		var json = JSON.new()
		json.parse(packet)
		packet = json.data

		if packet is Array:
			var type = packet.pop_front()
			match type:
				"PIDs":
					process_pids.append_array(packet)
				"KEY_INPUT":
					print(packet)
					if (packet != ""):
						var input = InputEventKey.new()
						if (packet == "s"):
							input.keycode = KEY_S
						elif (packet == "d"):
							input.keycode = KEY_D
						elif (packet == "space"):
							input.keycode = KEY_SPACE
							
						input.pressed = true
						Input.parse_input_event(input)
						
					
		else:
			push_error("Invalid type received!")

func server_start():
	server.listen(UDP_PORT)
	set_process(true)


func server_stop():
	server.stop()
	set_process(false)


func kill_processes():
	for pid in process_pids:
		OS.kill(pid)
