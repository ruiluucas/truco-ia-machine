# CardReader
Essa é a classe que tem como missão realizar a leitura das cartas e envia-las para os escopos de lógica do programa.

## Importação
```python
from ultralytics import YOLO
import logging
import statistics
```

## Classe
```python
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
        self.cardBuffer = []
        return modeCardBuffer
```

