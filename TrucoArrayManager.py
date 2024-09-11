import numpy as np
class TrucoArrayManager:
    # Se concentra todas as cartas disponíveis para o jogo, sendo o ID de cada uma delas sua localização no array.
    allCardsWithoutNaipe = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
    # COncentra todos os naipes disponíveis
    allCardsNaipe = ['C', 'H', 'S', 'D']

    vira = str()
    myCards = []
    myCardsWhichPlay = []
    myLastCardWithLocalId = 0
    adversaryCards = []

    # Recebe uma carta carta de baralho e retorna o nível de poder dela referente ao truco
    def cardsToForeignId(self, cards):
        def get_card_id(card):
            card_value = self.allCardsWithoutNaipe.index(card[0])

            if card_value >= 9:
                naipeId = self.allCardsNaipe.index(card[1])
                return 9 + naipeId
            else:
                return card_value

        if isinstance(cards, str):
            return get_card_id(cards)
        elif isinstance(cards, list):
            return [get_card_id(card) for card in cards]

    # Recebe um array de 3 sem os naipes cartas e retorna um array ordenado pelo nível de poder das cartas
    def alignCardsByPower(self, cards):
        return sorted(cards, key=lambda card: self.cardsToForeignId(card))

    # Seta a carta do vira
    def setVira(self, card):
        # Adiciona o vira na memória
        self.vira = card
        self.redefineAllCardsOrderWithVira(self.vira)

    # Recebe um número de 0 a 2, passando a carta do array de cartas na mão do robô para as cartas que ele jogou
    def playCard(self, cardIdByPower):
        myCardsAsc = self.alignCardsByPower(self.myCards)
        cardToPlay = myCardsAsc[cardIdByPower]
        self.myLastCardWithLocalId = self.myCards.index(myCardsAsc[cardIdByPower])
        self.myCardsWhichPlay.append(cardToPlay)
        self.myCards.pop(self.myCards.index(cardToPlay))

    def whoWin(self, botCard, adversaryCard):
        if self.cardsToForeignId(botCard) >= self.cardsToForeignId(adversaryCard):
            return 0
        else:
            return 1
    
    # Redefine a ordem das cartas de acordo com o vira, fazendo com que a carta seguinte ao vira se torne a mais forte do jogo
    def redefineAllCardsOrderWithVira(self, vira):
        viraForeignId = self.allCardsWithoutNaipe.index(vira[0])
        
        if viraForeignId == 9:
            strongerCard = self.allCardsWithoutNaipe[0]
            self.allCardsWithoutNaipe.pop(0)
        else: 
            strongerCard = self.allCardsWithoutNaipe[viraForeignId + 1]
            self.allCardsWithoutNaipe.pop(viraForeignId + 1)

        self.allCardsWithoutNaipe.append(strongerCard)
        self.allCardsWithoutNaipe.append(strongerCard)
        self.allCardsWithoutNaipe.append(strongerCard)
        self.allCardsWithoutNaipe.append(strongerCard)

truco = TrucoArrayManager()

    



