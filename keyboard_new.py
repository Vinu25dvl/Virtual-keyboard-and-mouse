import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

keyboard = Controller()
detector = HandDetector(detectionCon=1)

class Button:
    def __init__(self, first_pos, text, btn_size=[85, 85]):
        self.first_pos = first_pos
        self.text = text
        if text == ' ':     # if text is space
            self.btn_size = [284, 85]
        else:           # for other btns
            self.btn_size = btn_size
        
class key():    
    def __init__(self):
        self.cap=cv2.VideoCapture(0)
    def __del__(self):
        self.cap.release()
        return
    def virtual_keyboard(self):  
        finalText = ""
# all keys
        keys = [["q","w", "e", "r","t","y","u","i","o","p"],
        ["a", "s", "d", "f","g","h","j","k","l"],
        ["z", "x", "c", "v","b","n","m", " "]]
        
        
        buttonList = []
        for i in range(len(keys)):
            for x, key in enumerate(keys[i]): 
                 # enumerate return no of iterations
                buttonList.append(Button([100 * x + 80, 100 * i + 10], key))


        while True:
            success, img = self.cap.read()
    # flip image, to avoid mirrored
            img = cv2.resize(img, (1286,720))
            img = cv2.flip(img, 1)
            img = detector.findHands(img)  # find hand
            lmList,bboxInfo = detector.findPosition(img)  # land marks 

            for button in buttonList:
                x, y = button.first_pos
                w, h = button.btn_size
            # draw keys
                cv2.rectangle(img, button.first_pos, (x + w, y + h), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, button.text, (x + 18, y + 62), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 3)

    # check for finger tipacccc
            if lmList:
                for button in buttonList:
                    x, y = button.first_pos
                    w, h = button.btn_size

                    if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                # dark btn colors
                        cv2.rectangle(img, button.first_pos, (x + w, y + h), (150, 150, 150), cv2.FILLED)   # gray color
                        cv2.putText(img, button.text, (x + 18, y + 62), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 3)
                        l, _, _ = detector.findDistance(8, 12, img, draw=False) # distance between 2nd and 3rd fingers
                        print(l)
                # click the particular btn
                        if l < 30:
                    # change btn colors
                            keyboard.press(button.text)  # type on real keyboard
                            cv2.rectangle(img, button.first_pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)  # green color
                            cv2.putText(img, button.text, (x + 18, y + 62), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 3)
                            finalText += button.text
                            sleep(0.5)
            cv2.putText(img, finalText, (165, 400), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 3)
            _,jpg2=cv2.imencode('.jpg',img)
            return jpg2.tobytes()
