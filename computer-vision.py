import cv2
from ultralytics import YOLO
import logging
import numpy as np
import statistics
import random

# Carrega o modelo pré-treinado
logging.getLogger('ultralytics').setLevel(logging.WARNING)
model = YOLO('yolov8s_playing_cards.pt')

# Inicializa a câmera
cap = cv2.VideoCapture(0)
class Truco:
    allCards = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
    warning = 'Para comecar, preciso ler o vira'
    setBlack = False

    vira = []
    myCards = []
    myCardsWhichPlay = []
    cardBuffer = []
    adversaryCards = []
    whoStart = random.randint(0, 1)

    askTruco = False
    askTrucoSize = 0
    
    def begin(self):
        self.begin = True
    
    def addCard(self, card):
        if f'{card}' in self.vira or f'{card}' in self.myCards or f'{card}' in self.adversaryCards:
            return

        if not self.vira:
            self.vira.append(f'{card}')
            self.lastCardId = [1, 0]
            self.setBlack = True
            self.warning = f'Agora mostre minhas cartas, sem olhar. Faltam {abs(len(self.myCards) - 3)}'
            return
        
        elif len(self.myCards) < 3 and not self.myCardsWhichPlay:
            self.myCards.append(f'{card}')
            self.lastCardId = [2, abs(len(self.myCards) - 3)]

            if len(self.myCards) < 3:
                self.warning = f'Agora mostre minhas cartas, sem olhar. Faltam {abs(len(self.myCards) - 3)}'
                
            elif  len(self.myCards) == 3:
                self.warning = f'Que comece o jogo. '
                self.setBlack = False

                if self.whoStart == 0:
                    rd = random.randint(0, 2)
                    self.playCard(rd)                  
                    self.warning += f'Eu comeco, escolho a carta {rd + 1}. Mostre sua carta.'

                if self.whoStart == 1:
                    self.warning += 'Voce comeca.'

            return
        
        elif len(self.adversaryCards) < 3:
            self.adversaryCards.append(f'{card}')
            self.lastCardId = [2, abs(len(self.myCards) - 3)]

            if len(self.myCardsWhichPlay) is not 3:
                # Faço a leitura da IA para escolher a carta
                rd = random.randint(0, len(self.myCards))
                self.playCard(rd)                  
                self.warning = f'Escolho a carta {rd + 1}. Mostre sua carta.'

            if len(self.adversaryCards) is not 3:
                self.warning = f'Escolho a carta {rd + 1}. Mostre sua carta.'

            return
    
    def playCard(self, cardId):
        self.myCardsWhichPlay.append(self.myCards[cardId])
        self.myCards.pop(cardId)

truco = Truco()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    imagem_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(imagem_hsv)
    fator_aumento = 1.8
    s = np.clip(s * fator_aumento, 0, 255).astype(np.uint8)
    imagem_hsv_aumentada = cv2.merge([h, s, v])
    frame = cv2.cvtColor(imagem_hsv_aumentada, cv2.COLOR_HSV2BGR)

    # Realiza a predição
    results = model(frame)

    if truco.setBlack:
        frame[:] = 0

    # Verifica cada resultado que aparece
    for result in results:
        boxes = result.boxes

        if not boxes and truco.cardBuffer:
            truco.addCard(statistics.mode(truco.cardBuffer))
            truco.cardBuffer = []

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]

            # Qual carta está sendo predita
            label = result.names[int(box.cls)]
            truco.cardBuffer.append(label)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0))
    
    cv2.putText(frame, f'{truco.warning}', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
    cv2.putText(frame, f'{truco.warning}', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.putText(frame, f'Cartas que joguei: {truco.myCardsWhichPlay}', (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
    cv2.putText(frame, f'Cartas que joguei: {truco.myCardsWhichPlay}', (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.putText(frame, f'Cartas do adversário: {truco.adversaryCards}', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
    cv2.putText(frame, f'Cartas do adversário: {truco.adversaryCards}', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Truco Machine', frame)
    cv2.waitKey(100)
    
cap.release()
cv2.destroyAllWindows()