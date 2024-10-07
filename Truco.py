import random
import statistics
import numpy as np
import keyboard

from TrucoCardManager import TrucoCardManager

class Truco:
    command = 'Embaralhe as cartas e mostre-me o vira'
    warning = str()
    trucoLabel = str()

    isInitGame = True

    botPoints = 0
    userPoints = 0

    botPointInRound = 0
    userPointsInRound = 0

    whoStart = random.randint(0, 1)
    whoWinFirstRound = 2

    trucoProbability = 0
    trucoValue = 1
    empache = False

    cardReaderBlock = False

    def __init__(self):
        self.trucoCardManager = TrucoCardManager()
        self.keyboardInit()
    
    # Ativa os comandos de teclado
    def keyboardInit(self):
        # Irá responder a um pedido de truco do robô
        keyboard.on_press_key("d", lambda _: self.trucoAdversaryResponse(2))
        keyboard.on_press_key("a", lambda _: self.trucoAdversaryResponse(1))
        keyboard.on_press_key("r", lambda _: self.trucoAdversaryResponse(0))

        keyboard.on_press_key("z", lambda _: self.reset())

        # Irá pedir o truco e o robô tem de decidir se aceita, nega ou dobra
        keyboard.on_press_key("t", lambda _: self.trucoQuestion())

    # Método que reseta o round inteiro.
    def reset(self):
        self.botPointInRound = 0
        self.trucoValue = 1
        self.userPointsInRound = 0
        self.trucoCardManager.botCards = []
        self.trucoCardManager.playedBotCards = []
        self.trucoCardManager.userCards = []
        self.trucoCardManager.allCardsWithoutNaipe = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.trucoCardManager.vira = str()
        self.command = 'Embaralhe as cartas e mostre-me o vira'
        self.warning = str()
        self.trucoLabel = str()
        self.whoStart = random.randint(0, 1)
        self.cardReaderBlock = False
        return

    # Pergunta para o robô se ele aceita truco
    def trucoQuestion(self):
        # Aceita o truco baseado na probabilidade
        if self.percentGate(self.trucoProbability):
            self.trucoLabel = "O robo aceitou o truco"

            # Aumenta a aposta com base na mesma probabilidade, de forma que a probabilidade P dele aceitar é P ao quadrado
            if self.percentGate(self.trucoProbability):
                self.trucoLabel = "O robo quer aumentar a aposta"
                self.cardReaderBlock = True

            if self.trucoValue == 1:
                self.trucoValue = 3
            else:
                self.trucoValue += 3
        else:
            self.userPoints += 1
            self.trucoLabel = "O robô não aceitou o truco. Aperte Z para reiniciar"
            self.cardReaderBlock = True
        return
            
    # Função chamada pelos atalhos do teclado, podendo aceitar, pedir, dobrar e recusar truco
    def trucoAdversaryResponse(self, accept):
        if self.cardReaderBlock:
            self.cardReaderBlock = False

            if accept == 2:
                self.trucoLabel = "Adversario dobrou aposta do truco"
                self.trucoQuestion()
            elif accept == 1:
                if self.trucoValue == 1:
                    self.trucoValue = 3
                    self.trucoLabel = "Adversario aceitou a aposta do truco"

                    self.rollGame('')
                else:
                    self.trucoValue += 3
                    self.trucoLabel = "Adversario aceitou dobrar a aposta do truco"
                
            elif accept == 0:
                self.botPoints += 1
                self.trucoLabel = "Adversario nao aceitou truco. Aperte Z para recomeçar"
                self.cardReaderBlock = True
        return
        
    # Chamada para verificar se o vira já foi adicionado, mas as cartas do robô ainda não
    def blackGate(self):
        if self.trucoCardManager.vira and (len(self.trucoCardManager.botCards) != 3 and not self.trucoCardManager.playedBotCards):
            return True
        return False
    
    # Chamada para setar as cartas essenciais e configurações para a inicialização do jogo
    def rollInitGame(self, card):
        print("RollInitGame")
        if not self.trucoCardManager.vira:
            self.trucoCardManager.setVira(card)
            self.command = f'Agora mostre as cartas do robo. Faltam {abs(len(self.trucoCardManager.botCards) - 3)} cartas.'
            return
        
        self.trucoCardManager.botCards.append(card)
        if len(self.trucoCardManager.botCards) == 3: # Verifica se a carta que acabou de ser adicionada foi a última
            # Cria a probabilidade de pedir truco com base na média das cartas
            myCardsIdMean = statistics.mean(self.trucoCardManager.cardsToForeignId(self.trucoCardManager.botCards))
            self.trucoProbability = (1.944 * np.square(myCardsIdMean)) - (23.33 * myCardsIdMean) + 80 

            self.command = f'Cartas visualizadas. '

            if self.whoStart == 0:
                self.rollGame('')
            else:
                self.command += f'Voce comeca.'

            print(f'Vira: {self.trucoCardManager.vira}')
            print(f'Cartas do Robô: {self.trucoCardManager.botCards}')
        else:
            self.command = f'Faltam {abs(len(self.trucoCardManager.botCards) - 3)} cartas.'
        return
    
    # Caso não aja uma carta, ele apenas joga a carta
    def rollGame(self, card):
        print(f"RollGame {card}")
        
        if self.whoStart == 0:
            if card == '': # Verifica se o robô quem está começando o jogo, sendo representado pela chamada da função sem nenhum parâmetro
                if not self.cardReaderBlock:
                    self.trucoCardManager.playCard(random.randint(0, len(self.trucoCardManager.botCards) - 1))
                    self.command = f'Jogo a carta numero {str(self.trucoCardManager.lastBotCardWithLocalId)}'
            else:
                self.trucoCardManager.userCards.append(card)
                self.whoWinRound()
                self.checkRoundWinner()
                
                if self.trucoValue == 1: # Verifica se já foi pedido truco
                # Verifica se já foi pedido truco
                    if self.percentGate(self.trucoProbability):
                        self.trucoLabel = "Truco?"
                        self.cardReaderBlock = True

                if not self.cardReaderBlock:
                    if len(self.trucoCardManager.playedBotCards) != 3:
                        # Verifica se e a ultima carta do robo
                        if len(self.trucoCardManager.botCards) == 1:
                            self.trucoCardManager.playCard(0)
                            self.command = f'Jogo minha ultima carta.'
                        else:
                            self.trucoCardManager.playCard(random.randint(0, len(self.trucoCardManager.botCards) - 1))
                            self.command = f'Jogo a carta numero {str(self.trucoCardManager.lastBotCardWithLocalId)}'
                
        else:
            print("Adversário começa.")
            self.trucoCardManager.userCards.append(card)

            if self.trucoValue == 1: # Verifica se já foi pedido truco
                # Verifica se já foi pedido truco
                if self.percentGate(self.trucoProbability):
                    self.trucoLabel = "Truco?"
                    self.cardReaderBlock = True
                
            if not self.cardReaderBlock:
                if len(self.trucoCardManager.playedBotCards) != 3:
                    # Verifica se e a ultima carta do robo
                    if len(self.trucoCardManager.botCards) == 1:
                        self.trucoCardManager.playCard(0)
                        self.command = f'Jogo minha ultima carta.'
                    else:
                        self.trucoCardManager.playCard(random.randint(0, len(self.trucoCardManager.botCards) - 1))
                        self.command = f'Jogo a carta numero {str(self.trucoCardManager.lastBotCardWithLocalId)}'

            self.whoWinRound()
            self.checkRoundWinner()
        return       

    # Irá sortear um número com base na probabilidade passada como parâmetro
    def percentGate(self, percentageInPercentageRepresentation):
        if random.randint(0, 100) <= percentageInPercentageRepresentation:
            return True
        else:
            return False
    
    # Checa se houve ganhador, e caso houver, adiciona um ponto ao mesmo e reseta o round
    def checkRoundWinner(self):
        if self.botPointInRound > 1:
            self.trucoProbability = 0
            self.botPoints += self.trucoValue
            print(self.botPoints)
            self.warning += f'Pressione Z para recomecar'
            self.cardReaderBlock = True

        if  self.userPointsInRound > 1:
            self.trucoProbability = 0
            self.userPoints += self.trucoValue
            self.warning += f'Pressione Z para recomecar'
            self.cardReaderBlock = True
    
    def whoWinRound(self):
        print(f'botCard {self.trucoCardManager.playedBotCards[-1]}')
        print(f'userCard {self.trucoCardManager.userCards[-1]}')
        whoWin = self.trucoCardManager.whoWin(self.trucoCardManager.playedBotCards[-1], self.trucoCardManager.userCards[-1])

        if whoWin == 2:
            self.trucoProbability = 0
            if self.whoWinFirstRound == 2:
                self.warning = f'Empache na primeira. Mostre sua carta mais forte'
                self.empache = True
                return
            if self.whoWinFirstRound == 0:
                self.botPointInRound += 1
                self.warning = f'Empachou e ganhei a primeira'
                self.cardReaderBlock = True
                return
            if self.whoWinFirstRound == 1:
                self.userPointsInRound += 1
                self.warning = f'Empachou e voce ganhou a primeira'
                self.cardReaderBlock = True
                return
        if whoWin == 0:
            self.botPointInRound += 1
            self.whoWinFirstRound = 0
            self.warning = f'Ganhei a rodada!'
            return
        if whoWin == 1:
            self.userPointsInRound += 1
            self.whoWinFirstRound = 1
            self.warning = f'Voce ganhou a rodada!'
            return

    def isRepeatedCard(self, card):
        if card in (self.trucoCardManager.botCards + self.trucoCardManager.userCards + self.trucoCardManager.playedBotCards) or card == self.trucoCardManager.vira:
            return True
        return False