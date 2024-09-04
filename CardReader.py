from ultralytics import YOLO
import logging
import statistics

class CardReader:
    model = YOLO('../yolov8s_playing_cards.pt')
    cardBuffer = []

    def __init__(self):
        logging.getLogger('ultralytics').setLevel(logging.WARNING)
        return
    
    def detect(self, frame):
        return self.model(frame)
    
    def currentCard(self):
        modeCardBuffer = statistics.mode(self.cardBuffer)
        self.cardBuffer = []
        return modeCardBuffer