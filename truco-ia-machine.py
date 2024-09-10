# Importar bibliotecas
import cv2

# Importar classes externas
from FrameEditor import FrameEditor
from CardReader import CardReader
from Truco import Truco
from TrucoArrayManager import TrucoArrayManager

# Inicializa as classes necessárias
frameEditor = FrameEditor()
cardReader = CardReader()
truco = Truco()
trucoArrayManager = TrucoArrayManager()
    
# Inicializa o vídeo
cap = cv2.VideoCapture(0)
# Começa o loop para com os frames do vídeo
while True:
    # Realiza a leitura do frame e o transforma em uma matriz
    ret, frame = cap.read()
    if not ret:
        break
        
    # Realiza a mudança de saturação do frame para melhorar a indentificação da imagem
    frame = frameEditor.changeSaturation(frame, 1.8)

    # Realiza a verificação para fechar ou abrir a cãmera, dado esse recebido pela classe Truco
    frame = frameEditor.setBlackGate(frame, truco.blackGate())

    # Realiza a deteção das cartas no frame atual, retornando 
    frameData = cardReader.detect(frame)

    # Faz uma varredura em cada resultado
    for result in frameData:
        # Captura as caixas de seleção do respectivo resultado
        boxes = result.boxes

        # Caso não tenha cartas na tela e o buffer esteja cheio, já verifica qual carta é e adiciona
        if not boxes and cardReader.cardBuffer:
            if not truco.initGame:
                truco.rollInitGame(cardReader.currentCard())
            else:
                truco.rollGame(cardReader.currentCard())

        for box in boxes:
            frame = frameEditor.writeRectangle(frame, box)
            cardReader.cardBuffer.append(result.names[int(box.cls)])

    frame = frameEditor.setWarning(frame, truco.warning)
    frame = frameEditor.setActualGameLabel(frame, truco.trucoArrayManager.vira, truco.trucoArrayManager.myCardsWhichPlay, truco.trucoArrayManager.adversaryCards)
    cv2.imshow('Truco IA Machine', frame)
    cv2.waitKey(100)

cap.release()
cv2.destroyAllWindows()


        