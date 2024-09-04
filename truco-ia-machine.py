import cv2

from FrameEditor import FrameEditor
from CardReader import CardReader
from Truco import Truco

frameEditor = FrameEditor()
cardReader = CardReader()
truco = Truco()
    
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = frameEditor.changeSaturation(frame, 1.8)
    frameData = cardReader.detect(frame)
    frame = frameEditor.setBlackGate(frame, truco.blackGate())

    for result in frameData:
        boxes = result.boxes

        # Caso não tenha cartas na tela e o buffer esteja cheio, já verifica qual carta é e adiciona
        if not boxes and cardReader.cardBuffer:
            if not truco.initGame:
                truco.rollInitGame(cardReader.currentCard())
            else:
                truco.rollGame()

        for box in boxes:
            frame = frameEditor.writeRectangle(frame, box)
            cardReader.cardBuffer.append(result.names[int(box.cls)])

    frame = frameEditor.setWarning(frame, truco.warning)
    frame = frameEditor.setActualGameLabel(frame, truco.vira, truco.myCardsWhichPlay, truco.adversaryCards)
    cv2.imshow('Truco IA Machine', frame)
    cv2.waitKey(100)

cap.release()
cv2.destroyAllWindows()


        