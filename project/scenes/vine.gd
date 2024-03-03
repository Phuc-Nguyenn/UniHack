extends Area2D

var _player = null
var rotate = false
var rotation_total = 0

# Called when the node enters the scene tree for the first time.
func _ready():
	connect("body_entered", _on_body_entered)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if _player != null and _player.swinging:
		rotate = true
	
	if rotate:
		if rotation > -1:
			rotation -= 1.2 * delta
		else:
			_player.cannotSwing()

func _on_body_entered(other):
	if other.name == "Monkey":
		_player = other
		_player.canSwing()
		disconnect("body_entered", _on_body_entered)
