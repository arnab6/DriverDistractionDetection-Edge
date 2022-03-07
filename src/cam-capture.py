

import cv2


cam = cv2.VideoCapture(1)#reading camera feed 
cv2.namedWindow("test") #creating a window where images will be displayed 

img_counter = 0

while True:
    """
     The part of the code reads a frame , displays a frame 
     if space is pressed it stores that image into disk 
     to quit escpae needs to be pressed 
     
    """
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "uoh_clas_sleepy{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()
