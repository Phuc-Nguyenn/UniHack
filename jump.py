import cv2
import mediapipe as mp
import numpy as np
import time 

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


### CONSTANTS 
video_height = 720
video_width = 480



#Counter variables
counterDuck = 0 
counterJump = 0
counterSwing = 0
stageDuck = None
stageJump = None
stageSwing = None

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
    return angle 

cap = cv2.VideoCapture(0)


with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:   
    while cap.isOpened():
        
        ret, frame = cap.read()
        
        #Crop the video capture: 
        frame = frame[0:720, 360:840]

        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        image_height, image_width, _ = image.shape 
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            ### COORDINATES 
            #shoulder 
            right_shoulder = [landmarks[11].x,landmarks[11].y]
            left_shoulder = [landmarks[12].x,landmarks[12].y]

            #hip 
            right_hip = [landmarks[23].x,landmarks[23].y]
            left_hip = [landmarks[24].x,landmarks[24].y]

            #elbow 
            right_elbow = [landmarks[13].x,landmarks[13].y]
            left_elbow = [landmarks[14].x,landmarks[14].y]


            #Get the distance between shoulder and hip 
            hip_shoulder_distance = (right_shoulder[1] - right_hip[1] + left_shoulder[1] - left_hip[1]) / 2

            ## Coordinates in the main image: 
            right_shoulder_point = (int(right_shoulder[0] * image_width), int(right_shoulder[1] * image_height))
            left_shoulder_point = (int(left_shoulder[0] * image_width), int(left_shoulder[1] * image_height))

            #Shoulder line 
            cv2.line(image, (0, 210), (480, 210), (255, 0, 0), 2)
            #Jump line
            cv2.line(image, (0, 90), (480, 90), (255, 255, 0), 2)
            #Duck line
            cv2.line(image, (0, 300), (480, 300), (255, 0, 255), 2)
            

            # Calculate angle
            angleSwingRight = calculate_angle(right_elbow, right_shoulder, left_shoulder)
            angleSwingLeft = calculate_angle(left_elbow, left_shoulder, right_shoulder)
            print(angleSwingRight)



            ### LOGIC ###
            # Logic for ducking
            if right_shoulder[1] * video_height > 300: 
                stageDuck = "down"
            if stageDuck == "down": 
                #time.sleep(2)
                stageDuck = "up"
                counterDuck += 1

            # Logic for jumping
            if right_shoulder[1] * video_height < 90: 
                stageJump = "above"
            if stageJump == "above": 
                #time.sleep(0.1)
                stageJump = "back"
                counterJump += 1
            

            #Logic for swinging 
            if angleSwingLeft < 100 and angleSwingRight < 100: 
                stageSwing = "swing"
            if stageSwing == "swing":
                counterSwing += 1
                #time.sleep(0.05)
                stageSwing = "back"


        ### DEBUG ###
        #print(hip_shoulder_distance) 
        except:
            pass
        


        ### DISPLAYING ###
        # Setup status box
        cv2.rectangle(image, (0,0), (270,73), (245,117,16), -1)
        
        # TEXT to display
        cv2.putText(image, 'DUCK', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counterDuck), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        cv2.putText(image, 'JUMP', (105,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.putText(image, str(counterJump), 
                    (100,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        cv2.putText(image, 'SWING', (195,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.putText(image, str(counterSwing), 
                    (190,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()