import random
import statistics

class Truco:
    allCardsWithoutNaipe = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
    allCardsNaipe = ['C', 'H', 'S', 'D']
    
    myCards = []
    myCardsId = []
    myCardsAscAsc = []
    myCardsIdMean = 0
    myCardsWithoutNaipes = []
    warning = 'Deixe-me ler o vira'
    initGame = False

    vira = []
    viraIndex = 0
    viraWithoutNaipe = ''
    strongerCard = ''

    myCardsWhichPlay = []
    adversaryCards = []
    whoStart = random.randint(0, 1)
    phase = 0

    trucoProbability = 0
    askTruco = random.randint(1, 10)
    trucoValue = 0

    def blackGate(self):
        if self.vira and len(self.myCards) != 3:
            return True
        return False
    
    def rollInitGame(self, card):
        if card in (self.vira + self.myCards + self.adversaryCards):
            return
        
        if not self.vira:
            self.vira.append(card)
            self.viraWithoutNaipe = self.vira[0][0]
            self.viraIndex = self.allCardsWithoutNaipe.index(self.viraWithoutNaipe)

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

                if self.whoStart == 0:
                    self.warning = f'Começou o jogo. '
                    self.rollGame('')

                print('myCards: ' + self.myCards)
                print('myCardsId: ' + self.myCardsId)
                print('myCards: ' + self.myCardsIdMean)
            
            self.warning = f'Mostre minhas cartas. Faltam {abs(len(self.myCards) - 3)} cartas'
            return

        return
    
    def rollGame(self, card):
        if self.askTruco <= 8:
            self.askTruco = random.randint(1, 10)
        else:
            self.warning = 'TRUCO!!!'
            self.trucoValue += 3

        if card != '':
            self.adversaryCards.append(card)

            return
        
        return
    
    def playCard(self, cardId):
        self.myCardsWhichPlay.append(self.myCards[cardId])
        self.myCards.pop(cardId)

    def setAscCards(self, myCardsId):
        myCardsAsc = []
        for card in myCardsId:
            if len(myCardsAsc) == 0:
                myCardsAsc.append(card)
            else:
                inserted = False
                for i in range(len(myCardsAsc)):
                    if card < myCardsAsc[i]:
                        myCardsAsc.insert(i, card)
                        inserted = True
                        break
                if not inserted:
                    myCardsAsc.append(card)
                    break
        return myCardsAsc
    
    def setCardIds(self, myCards):
        myCardsId = []
        
        for id in range(0, 2):
            if self.allCardsWithoutNaipe.index(myCards[id][0]) >= 9:
                cardNaipe = myCards[id][1]
                cardNaipeId = self.allCardsWithoutNaipe.index(self.allCardsNaipe.index[cardNaipe])

                if cardNaipeId == 0:
                    myCardsId[id] = 9
                if cardNaipeId == 1:
                    myCardsId[id] = 10
                if cardNaipeId == 2:
                    myCardsId[id] = 11
                if cardNaipeId == 3:
                    myCardsId[id] = 12
            else:
                myCardsId[id] = self.allCardsWithoutNaipe.index(myCards[id][0])

        return myCardsId