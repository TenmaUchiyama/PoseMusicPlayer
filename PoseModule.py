import cv2 
import mediapipe as mp 
import time 
import math


class poseDetection():
    def __init__(self,mode=False,mode_complexity = 1,smooth_landmarks = True, min_detection_confidence=0.85,min_tracking_confidence = 0.85):
        self.static_image_mode = mode
        self.model_complexity = mode_complexity
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mp_pose = mp.solutions.pose
        self.poses = self.mp_pose.Pose(self.static_image_mode,self.model_complexity,self.smooth_landmarks,self.min_detection_confidence,self.min_tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        



    def findPose(self,img, draw=True):
        results = self.poses.process(img)
        if results.pose_landmarks and draw==True:
            self.mp_draw.draw_landmarks(img, results.pose_landmarks,self.mp_pose.POSE_CONNECTIONS)

        return img

    def findPosition(self, img, draw=False):
        self.lmList = [] 
        results = self.poses.process(img)
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList


    def findAngle(self, img, p1, p2, p3, draw=True):
       
            
        # # Get the landmarks
        x1 ,y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # print(angle)

        # # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle


        


