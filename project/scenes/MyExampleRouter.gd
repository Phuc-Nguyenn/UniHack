extends HttpRouter
class_name MyExampleRouter

func handle_get(request, response):
	if request.path == "/start_jumping":
		Input.action_press("ui_accept")
	if request.path == "/stop_jumping":
		Input.action_release("ui_accept")
	
	if request.path == "/start_swinging":
		Input.action_press("ui_down")
	if request.path == "/stop_swinging":
		Input.action_release("ui_down")
		
	if request.path == "/start_ducking":
		Input.action_press("ui_right")
	if request.path == "/stop_ducking":
		Input.action_release("ui_right")
		
	response.send(200, "Hello!")
