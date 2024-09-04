import random

class Truco:
    myCards = []
    warning = 'Deixe-me ler o vira'
    initGame = False

    vira = []
    myCardsWhichPlay = []
    adversaryCards = []
    whoStart = random.randint(0, 1)
    phase = 0

    askTruco = random.randint(1, 10)
    trucoValue = 0


    def blackGate(self):
        if self.vira and len(self.myCards) != 3:
            return True
        return False
    
    def rollInitGame(self, card):
        # Verifica se é carta repitida
        if card in (self.vira + self.myCards + self.adversaryCards):
            return
        
        if not self.vira:
            self.vira.append(card)
            self.warning = f'Mostre minhas cartas. Faltam {abs(len(self.myCards) - 3)} cartas'
            return
        
        if len(self.myCards) != 3:
            self.myCards.append(card)
            if len(self.myCards) is 3:
                self.warning = f'Cartas visualizadas.'
                self.initGame = True
                return
            self.warning = f'Mostre minhas cartas. Faltam {abs(len(self.myCards) - 3)} cartas'
            return
        return
    
    def rollGame(self):
        allCards = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']

        if self.askTruco <= 8:
            self.askTruco = random.randint(1, 10)
        else:
            self.warning = 'TRUCO!!!'
            self.trucoValue += 3

        myCardsWithoutNaipes = []
        for card in self.myCards:
            myCardsWithoutNaipes.append(card[0])
        
        return
    
    def playCard(self, cardId):
        self.myCardsWhichPlay.append(self.myCards[cardId])
        self.myCards.pop(cardId)