import random
import statistics
import numpy as np
import keyboard

from TrucoArrayManager import TrucoArrayManager

class Truco:
    command = 'Embaralhe as cartas e mostre-me o vira'
    warning = str()
    trucoLabel = str()

    isInitGame = True

    botPoints = 0
    adversaryPoints = 0

    botPointInRound = 0
    adversaryPointInRound = 0

    whoStart = random.randint(0, 1)

    trucoProbability = 0
    trucoValue = 1

    cardReaderBlock = False

    def __init__(self):
        self.trucoArrayManager = TrucoArrayManager()
        self.keyboardInit()
    
    # Ativa os comandos de teclado
    def keyboardInit(self):
        # Irá responder a um pedido de truco do robô
        keyboard.on_press_key("d", lambda _: self.trucoAdversaryResponse(2))
        keyboard.on_press_key("a", lambda _: self.trucoAdversaryResponse(1))
        keyboard.on_press_key("r", lambda _: self.trucoAdversaryResponse(0))

        # Irá pedir o truco e o robô tem de decidir se aceita, nega ou dobra
        keyboard.on_press_key("t", lambda _: self.trucoQuestion())

    # Método que reseta o round inteiro.
    def reset(self):
        self.botPointInRound = 0
        self.trucoValue = 1
        self.adversaryPointInRound = 0
        self.trucoArrayManager.myCards = []
        self.trucoArrayManager.myCardsWhichPlay = []
        self.trucoArrayManager.adversaryCards = []
        self.trucoArrayManager.allCardsWithoutNaipe = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.trucoArrayManager.vira = str()
        self.command = 'Embaralhe as cartas e mostre-me o vira'
        self.warning = str()
        self.trucoLabel = str()
        self.cardReaderBlock = False
        return

    # Pergunta para o robô se ele aceita truco
    def trucoQuestion(self):
        if self.percentGate(self.trucoProbability):
            self.trucoLabel = "Aceito! Pode jogar!"

            if self.percentGate(self.trucoProbability):
                self.trucoLabel = "Aumento a aposta! Aceita?"
                self.cardReaderBlock = True

            if self.trucoValue == 1:
                self.trucoValue = 3
            else:
                self.trucoValue += 3
        else:

            self.adversaryPoints += 1
            self.reset()
        return
            
    # Função chamada pelos atalhos do teclado, podendo aceitar, pedir, dobrar e recusar truco
    def trucoAdversaryResponse(self, accept):
        if self.cardReaderBlock:
            self.cardReaderBlock = False

            if accept == 2:
                self.trucoQuestion()
                self.trucoLabel = "Adversario dobrou aposta do truco"
            elif accept == 1:
                if self.trucoValue == 1:
                    self.trucoValue = 3
                    self.trucoLabel = "Adversario aceitou a aposta do truco"

                    if self.whoStart == 0:
                        self.rollGame('')
                else:
                    self.trucoValue += 3
                    self.trucoLabel = "Adversario aceitou dobrar a aposta do truco"
                
            elif accept == 0:
                self.botPoints += 1
                self.trucoLabel = "Adversario nao aceitou truco"
                self.reset()
        return
        
    # Chamada para verificar se o vira já foi adicionado, mas as cartas do robô ainda não
    def blackGate(self):
        if self.trucoArrayManager.vira and (len(self.trucoArrayManager.myCards) != 3 and not self.trucoArrayManager.myCardsWhichPlay):
            return True
        return False
    
    # Chamada para setar as cartas essenciais e configurações para a inicialização do jogo
    def rollInitGame(self, card):
        if not self.trucoArrayManager.vira:
            self.trucoArrayManager.setVira(card)
            self.command = f'Agora mostre as cartas do robo. Faltam {abs(len(self.trucoArrayManager.myCards) - 3)} cartas.'
            return
        
        if len(self.trucoArrayManager.myCards) != 3:
            self.trucoArrayManager.myCards.append(card)

            # Verifica se a carta que acabou de ser adicionada foi a última
            if len(self.trucoArrayManager.myCards) == 3:
                # Cria a probabilidade de pedir truco com base na média das cartas
                myCardsIdMean = statistics.mean(self.trucoArrayManager.cardsToForeignId(self.trucoArrayManager.myCards))
                self.trucoProbability = (1.944 * np.square(myCardsIdMean)) - (23.33 * myCardsIdMean) + 80 

                self.command = f'Cartas visualizadas. '

                if self.whoStart == 0:
                    self.rollGame('')
                else:
                    self.command += f'Voce comeca.'
            else:
                self.command = f'Faltam {abs(len(self.trucoArrayManager.myCards) - 3)} cartas.'
        return
    
    # Caso não aja uma carta, ele apenas joga a carta
    def rollGame(self, card):
        # Verifica se já foi pedido truco
        if self.trucoValue == 1:
            # Verifica se já foi pedido truco
            if self.percentGate(self.trucoProbability):
                self.trucoLabel = "Truco?"
                self.cardReaderBlock = True
        
        if not self.cardReaderBlock:
            # Verifica se o robô quem está começando o jogo, sendo representado pela chamada da função sem nenhum parâmetro
            if card == '':
                self.trucoArrayManager.playCard(random.randint(0, len(self.trucoArrayManager.myCards) - 1))
                self.command += f'Eu comeco. Jogo a carta numero {str(self.trucoArrayManager.myLastCardWithLocalId)}'
            else:
                self.trucoArrayManager.adversaryCards.append(card)
                
                if len(self.trucoArrayManager.myCardsWhichPlay) != 3:
                    # Verifica se e a ultima carta do robo
                    if len(self.trucoArrayManager.myCards) == 1:
                        self.trucoArrayManager.playCard(0)
                        self.command = f'Jogo minha ultima carta.'
                    else:
                        self.trucoArrayManager.playCard(random.randint(0, len(self.trucoArrayManager.myCards) - 1))
                        self.command = f'Jogo a carta numero {str(self.trucoArrayManager.myLastCardWithLocalId)}'
            
            if card != '':
                if self.trucoArrayManager.adversaryCards:
                    if self.whoStart == 0:
                        whoWIn = self.trucoArrayManager.whoWin(self.trucoArrayManager.myCardsWhichPlay[-1], self.trucoArrayManager.adversaryCards[-1])
                    else:
                        whoWIn = self.trucoArrayManager.whoWin(self.trucoArrayManager.myCardsWhichPlay[-1], self.trucoArrayManager.adversaryCards[-1])

                    if whoWIn == 0:
                        self.botPointInRound += 1
                        self.warning = f'Ganhei a rodada!'
                    if whoWIn == 1:
                        self.adversaryPointInRound += 1
                        self.warning = f'Voce ganhou a rodada!'
            return       

    # Irá sortear um número com base na probabilidade passada como parâmetro
    def percentGate(self, percentageInPercentageRepresentation):
        if random.randint(0, 100) <= percentageInPercentageRepresentation:
            return True
        else:
            return False
    
    # Checa se houve ganhador, e caso houver, adiciona um ponto ao mesmo e reseta o round
    def checkRoundWinner(self):
        if self.botPointInRound == 2 and self.isInitGame == False:
            self.botPoints += self.trucoValue
            self.warning = f'Ganhei a mão!'
            self.isInitGame = True

        if  self.adversaryPointInRound == 2 and self.isInitGame == False:
            self.adversaryPoints += self.trucoValue
            self.warning = f'Voce ganhou a mão!'
            self.isInitGame = True
    
    def isRepeatedCard(self, card):
        if card in (self.trucoArrayManager.myCards + self.trucoArrayManager.adversaryCards + self.trucoArrayManager.myCardsWhichPlay) or card == self.trucoArrayManager.vira:
            return True
        return False