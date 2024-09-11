import cv2
import numpy as np

class FrameEditor:
    def changeImage(self, frame, hue, saturation, value):
        imagem_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(imagem_hsv)

        h = np.clip(h * hue, 0, 255).astype(np.uint8)
        s = np.clip(s * saturation, 0, 255).astype(np.uint8)
        v = np.clip(v * value, 0, 255).astype(np.uint8)
        
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
    
    def addText(self, frame, text, color, positionFactor, fontSize):
        if color == 'black':
            rgbColor = (0, 0, 0)
            rgbBorder = (255, 255, 255)
        if color == 'white':
            rgbColor = (255, 255, 255)
            rgbBorder = (0, 0, 0)
        if color == 'red':
            rgbColor = (0, 0, 255)
            rgbBorder = (0, 0, 0)
        if color == 'blue':
            rgbColor = (255, 0, 0)
            rgbBorder = (0, 0, 0)
        if color == 'green':
            rgbColor = (0, 255, 0)
            rgbBorder = (0, 0, 0)
        
        frame = cv2.putText(frame, f'{text}', (5, (20 * positionFactor)), cv2.FONT_HERSHEY_SIMPLEX, fontSize, rgbBorder, 8)
        frame = cv2.putText(frame, f'{text}', (5, (20 * positionFactor)), cv2.FONT_HERSHEY_SIMPLEX, fontSize, rgbColor, 2)
        return frame
    
    def addLoading(self, frame, lenCardBuffer):
        if lenCardBuffer >= 25:
            lenCardBuffer = 100
            text = "Analise completa!"
        elif lenCardBuffer == 0:
            text = str()
        else:
            lenCardBuffer = lenCardBuffer * 4
            text = f'Lendo: {str(lenCardBuffer)}%'

        frame = cv2.putText(frame, f'{text}', (450, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
        frame = cv2.putText(frame, f'{text}', (450, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        return frame
