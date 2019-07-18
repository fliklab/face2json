from imutils import face_utils
import dlib
import cv2
import sys
import keyboard

p = "./landmark/shape_predictor_68_face_landmarks.dat"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

cap = cv2.VideoCapture(0)

timer = 0
outt = True
 
while True:
    timer=timer+1
    if (timer > 10000):
        timer=0
        outt=True

    # Getting out image by webcam 
    # _, image = cap.read()
    if(len(sys.argv) !=1 ):
        inputFile = "./" + sys.argv[1]
        image = cv2.imread(inputFile, 1)
    else:
        image = cv2.imread("./knowns/faces/face4.png", 1)

    # Converting the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # Get faces into webcam's image
    rects = detector(gray, 0)
    
    # For each detected face, find the landmark.
    for (i, rect) in enumerate(rects):
        # Make the prediction and transfom it to numpy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    
        # Draw circle on the cordinate points (x,y)
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        
        #outt=True

        #json start
        if(outt):
            finalJson = ""
            finalJson += '{\"face\":['

            n=0
            s=''
            for (x, y) in shape:
                n = n+1
                if(n == 68):
                    s = '[' + repr(x) + ',' + repr(y) + ']'
                    finalJson += s
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                else:
                    s = '[' + repr(x) + ',' + repr(y) + '],'
                    finalJson += s
                    sys.stdout.write('.')
                    sys.stdout.flush()

            #json end
            if(outt):
                finalJson += ']}'
                #print(finalJson, flush=True)

            jsonFile = 'outflie.json'
            jsonFile = outFile + '.json'
            if(len(sys.argv)>=2):
                outFile = sys.argv[2]

            fw = open(outFile, 'w')
            fw.write(finalJson)
            fw.close()
            msg = 'file saved in ' + outFile + '!'
            print(msg, flush = True)
    #break;

    outt=False

    # Show the image
    cv2.imshow("Output", image)

    # Save the image
    # imgOut = 'outFile.jpg'
    # imgOut = outFile + '.jpg'
    # cv2.im.Save("")

    k = cv2.waitKey(100) & 0xFF
    if k == 65:
        outt=True
    if k == 27:
        break


cv2.destroyAllWindows()
cap.release()
