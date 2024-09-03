def addSpecificCard(self, card):
    print(card)
    if(self.lastCardId[0] == 1):
        self.vira[0] = card
        return
    if(self.lastCardId[0] == 2):
        self.myCards[self.lastCardId[1]] = card
        return
    if(self.lastCardId[0] == 3):
        self.adversaryCards[self.lastCardId[1]] = card
        return
        
