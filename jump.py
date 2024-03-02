import cv2
import mediapipe as mp
import numpy as np
import time 

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


### CONSTANTS 
video_height = 720
video_width = 720


#Counter variables
counterDuck = 0 
counterJump = 0
counterSwing = 0
stageDuck = None
stageJump = None
stageSwing = None

#action status
inJump = False
inDuck = False
inSwing = False

#angle
left_angle = None
right_angle = None

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

shoulderQueue = []
averageInQueue = None

with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:   
    while cap.isOpened():
        
        ret, frame = cap.read()
        
        #Crop the video capture: 
        # frame = frame[0:720, 0:720]

        
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

            

            

            #changing decimals to coordinates
            right_shoulder_coords = [int(right_shoulder[0]*image_width), int(right_shoulder[1]*image_height)]
            left_shoulder_coords = [int(left_shoulder[0]*image_width), int(left_shoulder[1]*image_height)]
            right_hip_coords = [int(right_hip[0]*image_width), int(right_hip[1]*image_height)]
            left_hip_coords = [int(left_hip[0]*image_width), int(left_hip[1]*image_height)]
            right_elbow_coords = [int(right_elbow[0]*image_width), int(right_elbow[1]*image_height)]
            left_elbow_coords = [int(left_elbow[0]*image_width), int(left_elbow[1]*image_height)]

            #angle
            left_angle = calculate_angle(left_elbow_coords, left_shoulder_coords, left_hip_coords)
            right_angle = calculate_angle(right_elbow_coords, right_shoulder_coords, right_hip_coords)
            print("left angle: " + str(left_angle) +  "\n")
            # #print("\n")
            print("right angle: " + str(right_angle) + "\n")


            #averages
            shoulder_average_height = int((right_shoulder_coords[1] + left_shoulder_coords[1])/2)
            hip_average_height = int((right_hip_coords[1] + left_hip_coords[1])/2)
            torsoCenter = [int((right_shoulder_coords[0]+left_shoulder_coords[0]+right_hip_coords[0]+left_hip_coords[0])/4),
                           int((right_shoulder_coords[1]+left_shoulder_coords[1]+right_hip_coords[1]+left_hip_coords[1])/4)]

            
            nextJumpHeight = int(shoulder_average_height + (shoulder_average_height-hip_average_height)/4)
            #logic for changing the needed height for the jump, if the change between each frame is big then they are likely jumping
            #so we shouldn't update the height
            if len(shoulderQueue) > 0 and nextJumpHeight - shoulderQueue[-1] < (shoulder_average_height-hip_average_height)/6:
                shoulderQueue.append(shoulderQueue[-1])
            else:
                shoulderQueue.append(nextJumpHeight)
            
            #manage the "queue"
            if len(shoulderQueue) > 9 :
                isJumpHeight = shoulderQueue[0]
                shoulderQueue = shoulderQueue[1 : 9]

            # isJumpHeight = int(sum(shoulderQueue)/len(shoulderQueue))
            #needed height line
            cv2.line(image, (0, isJumpHeight), (1080, isJumpHeight), (255,0,0), 2)
            #shoulder line
            cv2.line(image, (0, shoulder_average_height), (1080, shoulder_average_height), (255,0,0), 2)
            # hip line
            cv2.line(image, (0, hip_average_height), (1080, hip_average_height), (255,0,0), 2)

            #logic for a jump
            if shoulder_average_height < isJumpHeight and inJump == False:
                counterJump += 1
                inJump = True
            elif shoulder_average_height > isJumpHeight:
                inJump = False

            #logic for a swing 
            if right_angle > 120 and left_angle > 120 and inSwing == False:
                counterSwing += 1
                inSwing = True
            elif right_angle < 120 and left_angle < 120: 
                inSwing = False 
            
            
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