import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


### CONSTANTS
VIDEO_HEIGHT = 720
VIDEO_WIDTH = 720


# Counter variables
counter_duck = 0
counter_jump = 0
counter_swing = 0

# action status
in_jump = False
in_duck = False
in_swing = False

# angle
left_angle = None
right_angle = None

# other variables
cap = cv2.VideoCapture(0)
jump_height_queue = []
prev_jump_height_queue = []
prev_jump_height = None


def calculate_angle(a, b, c):
    a = np.array(a)  # First point of angle
    b = np.array(b)  # Mid point of angle
    c = np.array(c)  # End point of angle

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
    return angle


with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
    while cap.isOpened():

        ret, frame = cap.read()

        # Crop the video capture:
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
            # shoulder
            right_shoulder = [landmarks[11].x, landmarks[11].y]
            left_shoulder = [landmarks[12].x, landmarks[12].y]

            # hip
            right_hip = [landmarks[23].x, landmarks[23].y]
            left_hip = [landmarks[24].x, landmarks[24].y]

            # elbow
            right_elbow = [landmarks[13].x, landmarks[13].y]
            left_elbow = [landmarks[14].x, landmarks[14].y]

            # changing decimals to integer coordinates
            right_shoulder_coords = [
                int(right_shoulder[0] * image_width),
                int(right_shoulder[1] * image_height),
            ]
            left_shoulder_coords = [
                int(left_shoulder[0] * image_width),
                int(left_shoulder[1] * image_height),
            ]
            right_hip_coords = [
                int(right_hip[0] * image_width),
                int(right_hip[1] * image_height),
            ]
            left_hip_coords = [
                int(left_hip[0] * image_width),
                int(left_hip[1] * image_height),
            ]
            right_elbow_coords = [
                int(right_elbow[0] * image_width),
                int(right_elbow[1] * image_height),
            ]
            left_elbow_coords = [
                int(left_elbow[0] * image_width),
                int(left_elbow[1] * image_height),
            ]

            # angle
            left_angle = calculate_angle(
                left_elbow_coords, left_shoulder_coords, left_hip_coords
            )
            right_angle = calculate_angle(
                right_elbow_coords, right_shoulder_coords, right_hip_coords
            )
            print("left angle: " + str(left_angle) + "\n")
            print("right angle: " + str(right_angle) + "\n")

            # averages
            shoulder_average_height = int(
                (right_shoulder_coords[1] + left_shoulder_coords[1]) / 2
            )
            hip_average_height = int((right_hip_coords[1] + left_hip_coords[1]) / 2)
            torsoCenter = [
                int(
                    (
                        right_shoulder_coords[0]
                        + left_shoulder_coords[0]
                        + right_hip_coords[0]
                        + left_hip_coords[0]
                    )
                    / 4
                ),
                int(
                    (
                        right_shoulder_coords[1]
                        + left_shoulder_coords[1]
                        + right_hip_coords[1]
                        + left_hip_coords[1]
                    )
                    / 4
                ),
            ]

            next_jump_height = int(
                shoulder_average_height
                + (shoulder_average_height - hip_average_height) / 4
            )
            prev_jump_height_queue.append(next_jump_height)
            if(len(prev_jump_height_queue) > 4) :
                prev_jump_height_queue = prev_jump_height_queue[1:4]

            # if the next_jump_height changes too quickly then we know that it is probably a jump
            if (
                len(jump_height_queue) > 6
                and abs(next_jump_height - prev_jump_height_queue[0])
                > (abs(shoulder_average_height - hip_average_height)) / 111
            ):
                # if its a jump then don't update next_jump_height
                jump_height_queue.append(jump_height_queue[-5])
                # val = abs(next_jump_height - prev_jump_height)
                # v2 = abs(shoulder_average_height - hip_average_height) / 18
                # print(str(val) + " " + str(v2) + " jumped so didn't update")
            else:
                jump_height_queue.append(next_jump_height)
                # print("didn't jump so it should move")
            
            prev_jump_height = next_jump_height

            # jump_height_queue.append(next_jump_height)
            # manage the "jump height queue" that tells you the threshhold for jumping
            if len(jump_height_queue) > 9:
                is_jump_height = jump_height_queue[0]
                jump_height_queue = jump_height_queue[1:9]

            is_duck_height = int(is_jump_height - (shoulder_average_height-hip_average_height)/2)
            # is_jump_height = int(sum(shoulderQueue)/len(shoulderQueue))
            # needed height jump line
            cv2.line(image, (0, is_jump_height), (1080, is_jump_height), (255, 255, 255), 2)
            # needed height duck line
            cv2.line(image, (0, is_duck_height), (1080, is_duck_height), (255, 255, 255), 2)

            # shoulder line
            cv2.line(
                image,
                (0, shoulder_average_height),
                (1080, shoulder_average_height),
                (255,0,0),
                2,
            )
            
            # hip line
            cv2.line(
                image,
                (0, hip_average_height),
                (1080, hip_average_height),
                (255, 0, 0),
                2,
            )

            # logic for a jump
            if shoulder_average_height < is_jump_height and in_jump == False:
                counter_jump += 1
                pyautogui.press("space")
                in_jump = True
            elif shoulder_average_height > is_jump_height:
                in_jump = False

            # logic for a swing
            if right_angle > 120 and left_angle > 120 and in_swing == False:
                counter_swing += 1
                in_swing = True
                pyautogui.press("s")
            elif right_angle < 120 and left_angle < 120:
                in_swing = False
            
        
            if shoulder_average_height < is_duck_height and in_duck == False:
                counter_duck += 1
                in_duck = True
                pyautogui.press("d")
            elif shoulder_average_height > is_duck_height and in_duck == True:
                in_duck = False

        except:
            pass

        ### DISPLAYING ###
        # Setup status box
        cv2.rectangle(image, (0, 0), (270, 73), (245, 117, 16), -1)

        # TEXT to display
        cv2.putText(
            image,
            "DUCK",
            (15, 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(counter_duck),
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.putText(
            image,
            "JUMP",
            (105, 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

        cv2.putText(
            image,
            str(counter_jump),
            (100, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.putText(
            image,
            "SWING",
            (195, 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

        cv2.putText(
            image,
            str(counter_swing),
            (190, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        # Render detections
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
        )

        cv2.imshow("Mediapipe Feed", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
