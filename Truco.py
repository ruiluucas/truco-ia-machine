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
    whoStart = 0 #random.randint(0, 1)
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
        
        listCard = list(card) 
        if(listCard[0] == '9'):
            listCard[0] = '6'
            card = str(listCard[0] + listCard[1])
        
        if not self.vira:
            self.vira.append(card)
            self.viraWithoutNaipe = self.vira[0][0]

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
                print("myCards")
                print(self.myCards)

                self.myCardsIdAsc = self.setCardIds(self.myCardsId)
                print("myCardsIdAsc")
                print(self.myCardsIdAsc)

                self.myCardsAsc = self.cardIdToCard(self.myCardsIdAsc)
                print("myCardsIdAsc")
                print(self.myCardsAsc)

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
            print('mycardo')
            print(self.myCardsAsc)
            self.playCard(random.randint(0, 1))
        else:
            self.adversaryCards.append(card)
            adversaryCardsMean = statistics.mean(self.setCardIds(self.adversaryCards))
            
        return
    
    def playCard(self, cardId):
        print(cardId)
        self.myCardsWhichPlay.append(self.myCardsAsc[cardId])
        print(self.myCardsWhichPlay)
        self.myCardsWhichPlayForeignId.append(self.myCards.index(self.myCardsAsc[cardId]))
        self.myCardsAsc.pop(cardId)

    def percentGate(self, percentageInPercentageRepresentation):
        if random.randint(0, 100) <= percentageInPercentageRepresentation:
            return True
        else:
            return False

    def setAscCards(self, cardsId):
        cardsIdAsc = []
        for cardId in cardsId:
            if len(cardsIdAsc) == 0:
                cardsIdAsc.append(cardId)
            else:
                inserted = False
                for i in range(len(cardsIdAsc)):
                    if cardId < cardsIdAsc[i]:
                        cardsIdAsc.insert(i, cardId)
                        inserted = True
                        break
                if not inserted:
                    cardsIdAsc.append(cardId)
                    break
        return cardsIdAsc
    
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
    
    def cardIdToCard(self, cardsId):
        cards = []
        
        for card in cardsId:
            self.allCardsWithoutNaipe.index(card)
            cards.append(self.allCardsWithoutNaipe[self.allCardsWithoutNaipe.index(card)])
            
        return cards