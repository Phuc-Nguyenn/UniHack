"""
Display the motion capture results in a GUI
"""

import camera

cam = camera.Camera(headless=False, debug=True)
cam.loop()
