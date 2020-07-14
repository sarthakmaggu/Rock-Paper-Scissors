from keras.models import load_model
import cv2
import numpy as np
from random import choice

shape_to_label = {'rock':np.array([1.,0.,0.]),'paper':np.array([0.,1.,0.]),'scissors':np.array([0.,0.,1.])}
arr_to_shape = {np.argmax(shape_to_label[x]):x for x in shape_to_label.keys()}

def winner(move1, move2):
    if move1 == move2:
        return "TIE"
    if move1 == "rock":
        if move2 == "scissors":
            return "User"
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return "User"
        if move2 == "scissors":
            return "Computer"

    if move1 == "scissors":
        if move2 == "paper":
            return "User"
        if move2 == "rock":
            return "Computer"

model = load_model("model.h5")
cv = cv2.VideoCapture(-1)
computer_move = None

while True:
    ret,frame = cv.read()
    cv.set(3,1280)
    cv.set(4,720)
    if not ret:
        continue
    #For user
    cv2.rectangle(frame,(100,100),(500,500),(0,255,255), 2)

    roi = frame[100:500, 100:500]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(roi,(300,300)).reshape(1,300,300,3)

    pred = model.predict(np.array(img))
    user_move = arr_to_shape[np.argmax(pred)]
    
    #Result
    if computer_move != user_move:
        if user_move != "none":
            computer_move = choice(["rock", "paper", "scissors"])
            result = winner(user_move,computer_move)
        else:
            computer_move = "none"
            result = "Waiting"
    
    font = cv2.FONT_HERSHEY_PLAIN

    #Displaying
    cv2.putText(frame, "Your Move: " + user_move,(50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Computer's Move: " + computer_move,(750, 50), font, 1., (0, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Winner: " + result,(400, 600), font, 2, (0, 0, 255), 4, cv2.LINE_AA)
    cv2.imshow("Rock Paper Scissors", frame)
    k = cv2.waitKey(10)
    if k == ord("q"):
        break
