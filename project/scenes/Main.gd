extends Node

const MONKEY_START_POS = Vector2i(150, 485)
const CAM_START_POS = Vector2i(576, 284)

var speed : float
var screen_size : Vector2i
var score : int
var time_out = 1
var time = time_out
var player_on_camera = false

const START_SPEED = 10.0
const MAX_SPEED = 25



# Called when the node enters the scene tree for the first time.
func _ready():
	screen_size = get_window().size
	new_game()


func new_game():
	# reset variables and nodes
	score = 0
	$Monkey.position = MONKEY_START_POS
	$Monkey.velocity = Vector2i(0, 0)
	$Camera2D.position = CAM_START_POS
	$ground.position = Vector2i(0, 0)
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if player_on_camera:
		speed = START_SPEED + score / 5
		
		# move camera and monkey
		$Monkey.position.x += speed
		$Camera2D.position.x += speed
		
		# update score
		if time > 0:
			time -= delta
		else:
			time = time_out
			score += 1
			show_score()
			
		
		# if ground finished
		if $Camera2D.position.x - $ground.position.x > screen_size.x * 1.5:
			$ground.position.x += screen_size.x
	else:
		# check if player is on camera and change this
		player_on_camera = true

func show_score():
	$scoredisplay.get_node("scorelabel").text = "SCORE: " + str(score)
	








