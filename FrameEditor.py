import cv2
import numpy as np

class FrameEditor:
    def changeSaturation(self, frame, factor):
        imagem_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(imagem_hsv)
        s = np.clip(s * factor, 0, 255).astype(np.uint8)
        imagem_hsv_aumentada = cv2.merge([h, s, v])
        frame = cv2.cvtColor(imagem_hsv_aumentada, cv2.COLOR_HSV2BGR)
        return frame
    
    def setBlackGate(self, frame, condition):
        if condition:
            frame[:] = 0
        return frame
    
    def writeRectangle(self, frame, box):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        frame = cv2.putText(frame, f'{box.conf[0]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0))
        return frame
    
    def setWarning(self, frame, warning):
        frame = cv2.putText(frame, f'{warning}', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
        frame = cv2.putText(frame, f'{warning}', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        return frame
    
    def setActualGameLabel(self, frame, vira, myCardsWhichPlay, adversaryCards):
        frame = cv2.putText(frame, f'Vira: {vira}', (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
        frame = cv2.putText(frame, f'Vira: {vira}', (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        frame = cv2.putText(frame, f'Robo: {myCardsWhichPlay}', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
        frame = cv2.putText(frame, f'Robo: {myCardsWhichPlay}', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        frame = cv2.putText(frame, f'Adversario: {adversaryCards}', (5, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
        frame = cv2.putText(frame, f'Adversario: {adversaryCards}', (5, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        return frame