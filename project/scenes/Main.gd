extends Node

var croc_scene = preload("res://scenes/crocodile.tscn")
var spike_scene = preload("res://scenes/spikes.tscn")
var eagle_scene = preload("res://scenes/bird.tscn")
var obstacle_types = [croc_scene, spike_scene]
var obstacles : Array
var eagle_heights = [300, 420]

const MONKEY_START_POS = Vector2i(150, 485)
const CAM_START_POS = Vector2i(576, 284)

var speed : float
var screen_size : Vector2i
var score : int
var time_out = 1
var time = time_out
var player_on_camera = false
var last_obstacle
var ground_height : int
var distance = 0
var last_obs_time = 0
var obs_timeout = 5
var difficulty = 0
var max_difficulty = 2.5


const START_SPEED = 10.0
const MAX_SPEED = 25



# Called when the node enters the scene tree for the first time.
func _ready():
	screen_size = get_window().size
	ground_height = $ground.get_node("Sprite2D").texture.get_height()
	$GameOver.get_node("Button").pressed.connect(new_game)
	new_game()


func new_game():
	# reset variables and nodes
	score = 0
	$Monkey.position = MONKEY_START_POS
	$Monkey.velocity = Vector2i(0, 0)
	$Camera2D.position = CAM_START_POS
	$ground.position = Vector2i(0, 0)
	get_tree().paused = false
	difficulty = 0
	
	# reset obstacles
	for obs in obstacles:
		obs.queue_free()
	obstacles.clear()
	
	$GameOver.hide()
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if player_on_camera:
		speed = START_SPEED + score / 10
		
		if speed > MAX_SPEED:
			speed = MAX_SPEED
		
		# generate obstacles
		last_obs_time -= delta
		if obstacles.is_empty() or last_obs_time < randi_range(0 + difficulty, 2 + difficulty):
			generate_obstacle()
		
		# move camera and monkey
		$Monkey.position.x += speed
		$Camera2D.position.x += speed
		
		for obs in obstacles:
			if obs.position.x < ($Camera2D.position.x - screen_size.x):
				obs.queue_free()
				obstacles.erase(obs)
		
		distance += speed
		
		# update score
		if time > 0:
			time -= delta
		else:
			time = time_out
			score += 1
			show_score()
			
		difficulty += score / 20
		if difficulty > max_difficulty:
			difficulty = max_difficulty
			
		
		# if ground finished
		if $Camera2D.position.x - $ground.position.x > screen_size.x * 1.5:
			$ground.position.x += screen_size.x
	else:
		# check if player is on camera and change this
		player_on_camera = true

func show_score():
	$scoredisplay.get_node("scorelabel").text = "SCORE: " + str(score)
	

func generate_obstacle():
	# if obstacles.is_empty() or last_obstacle.position.x < distance + randi_range(300, 500):
		var obstacle_type = obstacle_types[randi() % obstacle_types.size()]
		var obs = obstacle_type.instantiate()
		var obs_height = obs.get_node("Sprite2D").texture.get_height()
		var obs_scale = obs.get_node("Sprite2D").scale
		var obs_x = screen_size.x + distance + 100
		var obs_y = screen_size.y - ground_height - (obs_height * obs_scale.y / 2) + 5
		# obs.position = Vector2i(obs_x, obs_y)
		last_obstacle = obs
		add_obs(obs, obs_x, obs_y)
		last_obs_time = obs_timeout
		
		if difficulty > 0:
			if (randi() % 2) == 0:
				obs = eagle_scene.instantiate()
				obs_x = screen_size.x + distance + 100
				obs_y = eagle_heights[randi() % eagle_heights.size()]
				add_obs(obs, obs_x, obs_y)
		
func add_obs(obs, x, y):
	obs.position = Vector2i(x, y)
	obs.body_entered.connect(hit_obs)
	add_child(obs)
	obstacles.append(obs)
	
func hit_obs(body):
	if body.name == "Monkey":
		game_over()
		

func game_over():
	get_tree().paused = true
	$GameOver.show()
	
	# might have to be changed
	player_on_camera = false;
	






