import mediapipe as mp 
import time
from generate import Generate
import constants 
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
_, frm = cap.read()
height_ = frm.shape[0]
width_ = frm.shape[1]
gen = Generate(height_, width_)
s_init = False
s_time = time.time()
is_game_over = False

#declarations
hand = mp.solutions.hands
hand_model = hand.Hands(max_num_hands=1)
drawing = mp.solutions.drawing_utils

while True:
    ss = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    cv2.putText(frm, "score: "+str(gen.points), (width_ - 250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0,0), 3)

    # generate pipe every constants.TIME seconds
    if not(s_init):
        s_init = True 
        s_time = time.time()
    elif(time.time() - s_time) >= constants.GEN_TIME:
        s_init = False 
        gen.create()

    frm.flags.writeable = False
    res = hand_model.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    frm.flags.writeable = True

    #draw pipes && update there positions
    gen.draw_pipes(frm)
    gen.update()

    if res.multi_hand_landmarks:
        # hand is detected
        pts = res.multi_hand_landmarks[0].landmark
        # points = Points(pts)
        # grabbing index finger point
        index_pt = (int(pts[8].x * width_), int(pts[8].y * height_))

        if gen.check(index_pt): 
            # GAME OVER
            is_game_over = True
            frm = cv2.cvtColor(frm, cv2.COLOR_BGR2HSV)
            frm = cv2.blur(frm, (10, 10))
            cv2.putText(frm, "GAME_OVER!\nPress r to replay", (100, 100), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
            cv2.putText(frm, "Score : "+str(gen.points), (100, 180), cv2.FONT_HERSHEY_PLAIN, 4, (255,0,0), 3)
            gen.points = 0

        # bird
        cv2.circle(frm, index_pt, 20, (0, 0, 255), -1)
        # drawing.draw_landmarks(frm, res.multi_hand_landmarks[0], hand.HAND_CONNECTIONS)


    # cv2.putText(frm, "frame_rate: "+str(int(1/(time.time()-ss))), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("window", frm)
    
    if is_game_over:
        key_inp = cv2.waitKey(0)
        if(key_inp == ord('r')):
            is_game_over = False 
            gen.pipes = []
            constants.SPEED = 16
            constants.GEN_TIME = 1.2
        else :
            cv2.destroyAllWindows()
            cap.release()
            break

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break