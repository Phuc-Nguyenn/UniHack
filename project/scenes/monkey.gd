extends CharacterBody2D

const SPEED = 400.0
const JUMP_VELOCITY = -1150.0
const GRAVITY = 3500

var swinging = false
var ratio = 0
var waiting = false

# Get the gravity from the project settings to be synced with RigidBody nodes.
# var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _ready():
	swinging = false
	velocity.y = 0

func _physics_process(delta):
	# Add the gravity.
	if not is_on_floor():
		if waiting and (Input.is_action_pressed("ui_down") || Input.is_key_pressed(KEY_S)):
			swinging = true
			$AnimatedSprite2D.play("swinging")
			velocity.y = -JUMP_VELOCITY*0.4
			waiting = false
			
		if swinging == true:
			if (Input.is_action_pressed("ui_down") || Input.is_key_pressed(KEY_S)):
				velocity.y -= GRAVITY*0.4 * delta
			else:
				cannotSwing()
		else:
			velocity.y += GRAVITY * delta

	# Handle jump.
	if is_on_floor():
		$"Running-CollisionShape2D".disabled = false
		if Input.is_action_pressed("ui_accept"):
			velocity.y = JUMP_VELOCITY
			$AnimatedSprite2D.play("jumping")
		
		elif (Input.is_action_pressed("ui_right") || Input.is_key_pressed(KEY_D)):
			$AnimatedSprite2D.play("ducking")
			$"Running-CollisionShape2D".disabled = true
		else:
			$AnimatedSprite2D.play("running")
	
	move_and_slide()

func canSwing():
	waiting = true

func cannotSwing():
	swinging = false
	$AnimatedSprite2D.play("jumping")
