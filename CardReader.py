from ultralytics import YOLO
import logging
import statistics

class CardReader:
    # Declaração da rede neural YOLO com a rede neural pré carregada.
    model = YOLO('../yolov8s_playing_cards.pt')

    # Inicializa o buffer da carta
    cardBuffer = []

    # No momento em que a classe é chamada, é chamadado da importação "logging",
    # uma função para desabilitar logs desnecessários enquanto a detecção está acontecendo
    def __init__(self):
        logging.getLogger('ultralytics').setLevel(logging.WARNING)
        return

    # Realiza a deteção da carta e retorna a deteção
    def detect(self, frame):
        return self.model(frame)

    # Realiza o cálculo da mediana e zera o buffer, retornando a mediana do buffer recém zerado.
    def currentCard(self):
        modeCardBuffer = statistics.mode(self.cardBuffer)
        
        listCard = list(modeCardBuffer) 
        if(listCard[0] == '9'):
            listCard[0] = '6'
            modeCardBuffer = str(listCard[0] + listCard[1])

        self.cardBuffer = []
            
        return modeCardBuffer