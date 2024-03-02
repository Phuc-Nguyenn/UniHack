import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


### CONSTANTS 
ratio = 0.1 #The ratio of shoulder and hip distance 
shoulder_y_value = []


# Curl counter variables
counterDuck = 0 
counterJump = 0
counterSwing = 0
stageSquat = None
stageJump = None

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


# Set the desired width and height
new_width = 
new_height = 720

if cap.isOpened():
    # Get the current width and height of the video capture
    current_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    current_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set the new resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)


## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:   
    while cap.isOpened():
        ret, frame = cap.read()
        
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


            #Get the distance between shoulder and hip 
            hip_shoulder_distance = (right_shoulder[1] - right_hip[1] + left_shoulder[1] - left_hip[1]) / 2

            ## Coordinates in the main image: 
            right_shoulder_point = (int(right_shoulder[0] * image_width), int(right_shoulder[1] * image_height))
            left_shoulder_point = (int(left_shoulder[0] * image_width), int(left_shoulder[1] * image_height))


            cv2.line(image, right_shoulder_point, left_shoulder_point, (255, 0, 0), 5)
            print(right_shoulder[1])
            shoulder_y_value.append(right_shoulder[1])
            



            # Calculate angle
            angle1 = calculate_angle(right_hip, right_knee, right_ankle) #angle to detect squat
            #angle2 = calculate_angle(left_hip, left_knee, left_ankle) #angle to detect squat
            angle3 = calculate_angle(right_elbow, right_shoulder, right_hip) #angle to detect jumping jacks 


            ### LOGIC ###

            # Logic for ducking
            

            #Logic for jumping
            lastDistance = (shoulder_y_value[-1] - shoulder_y_value[-20])  #the distance for the last 10 pixel
            if lastDistance > (hip_shoulder_distance * ratio): 
                counterJump += 1
            print(lastDistance)


            #Logic for swinging 
        ### DEBUG 
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