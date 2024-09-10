import random
import statistics
import numpy as np

from TrucoArrayManager import TrucoArrayManager

class Truco:
    warning = 'Deixe-me ler o vira'
    initGame = False

    whoStart = random.randint(0, 1)
    phase = 0

    trucoProbability = 0
    trucoValue = 0

    def __init__(self):
        self.trucoArrayManager = TrucoArrayManager()

    def blackGate(self):
        if self.trucoArrayManager.vira and (len(self.trucoArrayManager.myCards) != 3 or self.trucoArrayManager.myCardsWhichPlay):
            return True
        return False
    
    def rollInitGame(self, card):
        listCard = list(card) 
        if(listCard[0] == '9'):
            listCard[0] = '6'
            card = str(listCard[0] + listCard[1])
        
        if not self.trucoArrayManager.vira:
            self.trucoArrayManager.setVira(card)
            self.warning = f'Agora mostre minhas cartas. Faltam {abs(len(self.trucoArrayManager.myCards) - 3)} cartas.'
            return
        
        if len(self.trucoArrayManager.myCards) != 3:
            self.trucoArrayManager.myCards.append(card)

            if len(self.trucoArrayManager.myCards) == 3:
                self.warning = f'Cartas visualizadas.'
                self.initGame = True

                myCardsIdMean = statistics.mean(self.trucoArrayManager.cardsToForeignId(self.trucoArrayManager.myCards))
                self.trucoProbability = (1.944 * np.square(myCardsIdMean)) - (23.33 * myCardsIdMean) + 80 

                if self.whoStart == 0:
                    self.rollGame('')
                return
            
            self.warning = f'Mostre minhas cartas. Faltam {abs(len(self.trucoArrayManager.myCards) - 3)} cartas.'
            return
        return
    
    def rollGame(self, card):
        if self.percentGate(self.trucoProbability):
            self.warning = 'TRUCO!!!'
            self.trucoValue += 3

        roboStarted = card == ''
        if roboStarted:
            self.trucoArrayManager.playCard(random.randint(0, 1))
        else:
            self.trucoArrayManager.adversaryCards.append(card)
        return        

    def percentGate(self, percentageInPercentageRepresentation):
        if random.randint(0, 100) <= percentageInPercentageRepresentation:
            return True
        else:
            return False