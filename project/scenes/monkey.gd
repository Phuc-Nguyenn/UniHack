extends CharacterBody2D


const SPEED = 400.0
const JUMP_VELOCITY = -1100.0
const GRAVITY = 3500

# Get the gravity from the project settings to be synced with RigidBody nodes.
# var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


func _physics_process(delta):
	# Add the gravity.
	if not is_on_floor():
		velocity.y += GRAVITY * delta

	# Handle jump.
	if is_on_floor():
		$"Running-CollisionShape2D".disabled = false
		if Input.is_action_pressed("ui_accept"):
			velocity.y = JUMP_VELOCITY
			$AnimatedSprite2D.play("jumping")
		
		elif Input.is_action_pressed("ui_down"):
			$AnimatedSprite2D.play("ducking")
			$"Running-CollisionShape2D".disabled = true
		else:
			$AnimatedSprite2D.play("running")

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	var direction = Input.get_axis("ui_left", "ui_right")
	if direction:
		velocity.x = direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)

	move_and_slide()
