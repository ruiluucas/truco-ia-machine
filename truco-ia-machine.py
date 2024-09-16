# Importar bibliotecas
import cv2

# Importar classes externas
from FrameEditor import FrameEditor
from CardReader import CardReader
from Truco import Truco

# Inicializa as classes necessárias
frameEditor = FrameEditor()
cardReader = CardReader()
truco = Truco()
    
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = frameEditor.changeImage(frame, 1, 1.4, 1)

    if not truco.cardReaderBlock:
        frameData = cardReader.detect(frame)
        
        frame = frameEditor.setBlackGate(frame, truco.blackGate())

        for result in frameData:
            boxes = result.boxes
            
            if not boxes and len(cardReader.cardBuffer) > 25: # Não está tendo seleção e o cardBuffer está cheio
                # Verifica a carta que foi obtida do buffer
                currentCard = cardReader.currentCard() # Armazena a carta que foi obtida do buffer

                if not truco.isRepeatedCard(currentCard): # Vefifica se a carta que foi obtida é repetida
                    if truco.empache:
                        strongerBotCard = truco.trucoCardManager.alignCardsByPower(truco.trucoCardManager.botCards)
                        whoWin = truco.trucoCardManager.whoWin(strongerBotCard[-1], currentCard)

                        if whoWin == 2:
                            truco.trucoCardManagerallCardsWithoutNaipe = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
                            truco.trucoCardManager.redefineAllCardsOrderWithVira(strongerBotCard)

                            whoWin = truco.trucoCardManager.whoWin(strongerBotCard[-1], currentCard)

                        if whoWin == 0:
                            truco.botPointInRound += 1
                            truco.warning = f'Ganhei o empache!'
                        if whoWin == 1:
                            truco.userPointsInRound += 1
                            truco.warning = f'Voce ganhou o empache!'
                        truco.checkRoundWinner()

                    if truco.trucoCardManager.roundIsEnableToStart():
                        truco.rollGame(currentCard)
                    else:
                        truco.rollInitGame(currentCard) # Adiciona a carta do vira e do robô
            else:          
                # Desenha o retângulo e adiciona ao buffer carta corrente
                for box in boxes:
                    frame = frameEditor.writeRectangle(frame, box)
                    frameName = result.names[int(box.cls)]

                    if not truco.isRepeatedCard(frameName):
                        cardReader.cardBuffer.append(frameName)
    
    frame = frameEditor.addLoading(frame, len(cardReader.cardBuffer))
    frame = frameEditor.addText(frame, "Truco Machine", 'red', 1, 0.8)
    frame = frameEditor.addText(frame, truco.command, 'white', 2, 0.6)
    frame = frameEditor.addText(frame, truco.warning, 'white', 3, 0.6)
    frame = frameEditor.addText(frame, f' Vira: {truco.trucoCardManager.vira}', 'white', 5, 0.6)
    frame = frameEditor.addText(frame, f' Cartas do robo: {truco.trucoCardManager.playedBotCards}', 'white', 6, 0.6)
    frame = frameEditor.addText(frame, f' Cartas do adversario: {truco.trucoCardManager.userCards}', 'white', 7, 0.6)
    frame = frameEditor.addText(frame, f' Pontos: Robo: {truco.botPoints} | Adversario: {truco.userPoints}', 'green', 9, 0.7)
    frame = frameEditor.addText(frame, f' Partida: Robo: {truco.botPointInRound} | Adversario: {truco.userPointsInRound}', 'green', 10, 0.5)
    frame = frameEditor.addText(frame, f' VaLOR DA RODADA: {truco.trucoValue}', 'black', 13, 0.5)
    frame = frameEditor.addText(frame, f'{truco.trucoLabel}', 'red', 15, 0.8)

    cv2.imshow('Truco IA Machine', frame)
    cv2.waitKey(50)

cap.release()
cv2.destroyAllWindows()


        