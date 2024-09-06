import random
import statistics
import numpy as np

class Truco:
    allCardsWithoutNaipe = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
    allCardsNaipe = ['C', 'H', 'S', 'D']
    
    myCards = []
    myCardsId = []
    myCardsAsc = []
    myCardsIdMean = 0
    myCardsWithoutNaipes = []
    warning = 'Deixe-me ler o vira'
    initGame = False

    vira = []
    viraIndex = 0
    viraWithoutNaipe = ''
    strongerCard = ''

    myCardsWhichPlay = []
    myCardsWhichPlayForeignId = []
    adversaryCards = []
    adversaryCardsIdMean = []
    whoStart = random.randint(0, 1)
    phase = 0

    trucoProbability = 0
    trucoValue = 0

    def blackGate(self):
        if self.vira and (len(self.myCards) != 3 or self.myCardsWhichPlay):
            return True
        return False
    
    def rollInitGame(self, card):
        if card in (self.vira + self.myCards + self.adversaryCards):
            return
        
        if(card[0][0] == '9'):
            card[0][0] = '6'
        
        if not self.vira:
            self.vira.append(card)
            self.viraWithoutNaipe = self.vira[0][0]
            print(f"{card} não foi encontrado na lista.")

            if self.viraIndex == 9:
                self.strongerCard = self.allCardsWithoutNaipe[0]
                self.allCardsWithoutNaipe.pop(0)
            else:
                self.strongerCard = self.allCardsWithoutNaipe[self.viraIndex + 1]
                self.allCardsWithoutNaipe.pop(self.viraIndex + 1)

            self.allCardsWithoutNaipe.append(self.strongerCard)
            self.allCardsWithoutNaipe.append(self.strongerCard)
            self.allCardsWithoutNaipe.append(self.strongerCard)
            self.allCardsWithoutNaipe.append(self.strongerCard)

            self.warning = f'Mostre minhas cartas. Faltam {abs(len(self.myCards) - 3)} cartas'
            return
        
        if len(self.myCards) != 3:
            self.myCards.append(card)

            if len(self.myCards) == 3:
                self.warning = f'Cartas visualizadas.'
                self.initGame = True

                for card in self.myCards:
                    self.myCardsWithoutNaipes.append(card[0])

                self.myCardsId = self.setCardIds(self.myCards)
                self.myCardsIdAsc = self.setAscCards(self.myCardsId)
                self.myCardsIdMean = statistics.mean(self.myCardsIdAsc)

                self.trucoProbability = (1.944 * np.square(self.myCardsIdMean)) - (23.33 * self.myCardsIdMean) + 80 

                if self.whoStart == 0:
                    self.rollGame('')
                return
            
            self.warning = f'Mostre minhas cartas. Faltam {abs(len(self.myCards) - 3)} cartas'
            return
        return
    
    def rollGame(self, card):
        if self.percentGate(self.trucoProbability):
            self.warning = 'TRUCO!!!'
            self.trucoValue += 3

        if card == '':
            self.playCard(random.randint(0, 1))
        else:
            self.adversaryCards.append(card)
            adversaryCardsMean = statistics.mean(self.setCardIds(self.adversaryCards))
            

        self.playCard(random.randint(0, len(self.myCards) - 1))

        return
    
    def playCard(self, cardId):
        self.myCardsWhichPlay.append(self.myCardsAsc[cardId])
        self.myCardsWhichPlayForeignId.append(self.myCards.index(self.myCardsAsc[cardId]))
        self.myCardsAsc.pop(cardId)

    def percentGate(self, percentageInPercentageRepresentation):
        if random.randint(0, 100) <= percentageInPercentageRepresentation:
            return True
        else:
            return False

    def setAscCards(self, cardsId):
        cardsAsc = []
        for card in cardsId:
            if len(cardsAsc) == 0:
                cardsAsc.append(card)
            else:
                inserted = False
                for i in range(len(cardsAsc)):
                    if card < cardsAsc[i]:
                        cardsAsc.insert(i, card)
                        inserted = True
                        break
                if not inserted:
                    cardsAsc.append(card)
                    break
        return cardsAsc
    
    def setCardIds(self, cards):
        cardsId = [0, 0, 0]
        
        for id in range(0, len(cards)):
            cards[id]
            if self.allCardsWithoutNaipe.index(cards[id][0]) >= 9:
                cardNaipe = self.myCards[id][1]
                naipeId = self.allCardsNaipe.index(cardNaipe)

                if naipeId == 0:
                    cardsId[id] = 9
                if naipeId == 1:
                    cardsId[id] = 10
                if naipeId == 2:
                    cardsId[id] = 11
                if naipeId == 3:
                    cardsId[id] = 12
            else:
                cardsId[id] = self.allCardsWithoutNaipe.index(cards[id][0])

        return cardsId