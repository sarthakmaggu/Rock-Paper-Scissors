import cv2
import sys
import os

try:
    name = sys.argv[1] #For taking command line arguments.
    number = int(sys.argv[2])
except:
    print("Please enter valid arguments")
    exit(-1)

folder_name = "data"
path = os.path.join(folder_name,name)

try:
    os.mkdir(folder_name)
except FileExistsError:
    pass

try:
    os.mkdir(path)
except FileExistsError:
    print("Directory already exists")

cv = cv2.VideoCapture(-1)
start = False
count = 0

while True:
    ret,frame = cv.read() #Two values return and image, if we get a return value then only we can use it.
    cv.set(3,1280)
    cv.set(4,720)
    if not ret:
        continue
    if count == number:
        break
    cv2.rectangle(frame,(100,100),(500,500),(0,255,255), 2) #First parameter is image on which box, next starting coordinates, ending coordinates, color and thickness.
    if start:
        ro = frame[100:500, 100:500]
        save = os.path.join(path, "{}.jpg".format(count+1))
        cv2.imwrite(save,ro)
        count += 1
    
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(frame, "Enter s to start collecting images", (0,10), font, 1,(0,255,255),2, cv2.LINE_AA) #Check documentation.py
    cv2.putText(frame, "Enter q to quit", (0,60), font, 1, (0,255,255), 2, cv2.LINE_AA)
    cv2.imshow("Images", frame)

    key = cv2.waitKey(10)
    if key == ord("s"):
        start = not start
    if key == ord("q"):
        break

print("Images saved")
cv.release()
cv2.destroyAllWindows()


    
