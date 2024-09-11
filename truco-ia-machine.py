# Importar bibliotecas
import cv2
import keyboard

# Importar classes externas
from FrameEditor import FrameEditor
from CardReader import CardReader
from Truco import Truco

# Inicializa as classes necessárias
frameEditor = FrameEditor()
cardReader = CardReader()
truco = Truco()
    
# Inicializa o vídeo
cap = cv2.VideoCapture(0)
# Começa o loop para com os frames do vídeo
while True:
    # Realiza a leitura do frame e o transforma em uma matriz
    ret, frame = cap.read()
    if not ret:
        break
        
    # Realiza a mudança de saturação do frame para melhorar a indentificação da imagem
    frame = frameEditor.changeImage(frame, 1, 1.4, 1)

    # Verifica se a leitura está bloqueada
    if not truco.cardReaderBlock:
        # Realiza a deteção das cartas no frame atual, retornando 
        frameData = cardReader.detect(frame)

        # Realiza a verificação para fechar ou abrir a cãmera, dado esse recebido pela classe Truco
        frame = frameEditor.setBlackGate(frame, truco.blackGate())

        # Faz uma varredura em cada resultado
        for result in frameData:
            # Captura as caixas de seleção do respectivo resultado
            boxes = result.boxes
            
            # Caso não tenha cartas na tela e o buffer esteja cheio, já verifica qual carta é e adiciona
            if not boxes and len(cardReader.cardBuffer) > 25:
                currentCard = cardReader.currentCard()
                
                if truco.isInitGame:
                    truco.reset()
                    truco.isInitGame = False

                if not truco.isRepeatedCard(currentCard):
                    if not len(truco.trucoArrayManager.myCards) == 3 and not truco.trucoArrayManager.myCardsWhichPlay:
                        truco.rollInitGame(currentCard)
                    else:
                        truco.rollGame(currentCard)


            # Desenha o retângulo e adiciona ao buffer carta corrente
            for box in boxes:
                frame = frameEditor.writeRectangle(frame, box)
                currentCardName = result.names[int(box.cls)]

                if not truco.isRepeatedCard(currentCardName):
                    cardReader.cardBuffer.append(currentCardName)

    # Verifica caso alguém tenha ganhado
    truco.checkRoundWinner()

    frame = frameEditor.addLoading(frame, len(cardReader.cardBuffer))

    frame = frameEditor.addText(frame, "Truco Machine", 'red', 1, 0.8)
    frame = frameEditor.addText(frame, truco.command, 'white', 2, 0.6)
    frame = frameEditor.addText(frame, truco.warning, 'white', 3, 0.6)

    frame = frameEditor.addText(frame, f' Vira: {truco.trucoArrayManager.vira}', 'blue', 5, 0.6)
    frame = frameEditor.addText(frame, f' Cartas do robo: {truco.trucoArrayManager.myCardsWhichPlay}', 'blue', 6, 0.6)
    frame = frameEditor.addText(frame, f' Cartas do adversario: {truco.trucoArrayManager.adversaryCards}', 'blue', 7, 0.6)

    frame = frameEditor.addText(frame, f' Pontos: Robo: {truco.botPoints} | Adversario: {truco.adversaryPoints}', 'green', 9, 0.7)
    frame = frameEditor.addText(frame, f' Na partida: Robo fez {truco.botPointInRound} | Adversario fez {truco.adversaryPointInRound}', 'green', 10, 0.7)

    frame = frameEditor.addText(frame, f' VaLOR DA RODADA: {truco.trucoValue}', 'black', 13, 0.5)
    frame = frameEditor.addText(frame, f'{truco.trucoLabel}', 'red', 15, 0.8)

    '''
    frame = frameEditor.setWarning(frame, truco.warning)
    frame = frameEditor.setActualGameLabel(frame, f'Vira: {truco.trucoArrayManager.vira}', 0)
    frame = frameEditor.setActualGameLabel(frame, f'Cartas do robo: {truco.trucoArrayManager.myCardsWhichPlay}', 2)
    frame = frameEditor.setActualGameLabel(frame, f'Cartas do adversario: {truco.trucoArrayManager.adversaryCards}', 3)
    frame = frameEditor.setActualGameLabel(frame, f'Valor da rodada: {truco.trucoValue}', 5)
    frame = frameEditor.setActualGameLabel(frame, f'Robo: {truco.botPoints} | Adversario: {truco.adversaryPoints}', 7)
    '''
    cv2.imshow('Truco IA Machine', frame)
    cv2.waitKey(50)

cap.release()
cv2.destroyAllWindows()


        