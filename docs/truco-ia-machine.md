# Projeto: Truco IA Machine

Este projeto utiliza visão computacional para detectar cartas de truco em tempo real por meio de uma webcam. Ele é responsável por detectar as cartas e gerenciar o estado do jogo de truco automaticamente.

## Dependências:

- Python 3.x
- OpenCV
- FrameEditor
- CardReader
- Truco

## Instalação:

1. Clone o repositório do projeto.
2. Instale as dependências necessárias executando o comando:

```bash
pip install opencv-python ultralytics logging statistics
```

<hr />

## Inicialização

O código inicia com a importação das bibliotecas e a inicialização das classes que controlam as principais funcionalidades do jogo:

```python
# Importar bibliotecas
import cv2

# Importar classes externas
from FrameEditor import FrameEditor
from CardReader import CardReader
from Truco import Truco

# Inicializa as classes necessárias
frameEditor = FrameEditor()
cardReader = CardReader()
truco = Truco()
```
#### As classes principais do projeto são:
- <strong>FrameEditor</strong>: Cuida das regras relacionadas à câmera. Controla a ativação e desativação, ajusta parâmetros como saturação, e desenha retângulos e textos na tela.
- <strong>CardReader</strong>: Responsável pela detecção de cartas no frame da câmera, utilizando IA para identificar as cartas em jogo.
- <strong>Truco</strong>: Gerencia a lógica do jogo, incluindo as cartas do robô e do adversário, a "vira", o nível de poder das cartas, e decide qual carta jogar.

<hr />

### Captura de Vídeo

O código abaixo inicializa a captura de vídeo através da webcam, utilizando um loop infinito para processar os frames em tempo real:

```python
# Inicializa o vídeo
cap = cv2.VideoCapture(0)

# Loop de captura de frames
while True:
    # Captura o frame e o converte em uma matriz
    ret, frame = cap.read()

    # Verifica se a captura foi bem-sucedida
    if not ret:
        break

    # Processa o frame (resto do código)

# Libera a webcam ao encerrar o programa
cap.release()

# Fecha todas as janelas abertas
cv2.destroyAllWindows()
```

Este trecho configura a câmera do computador para começar a capturar imagens. O OpenCV utiliza um loop infinito para capturar continuamente os frames, processando-os até que a execução seja interrompida.

<hr />

## Processamento do Frame
Dentro do loop principal, o frame capturado passa por ajustes, como a modificação da saturação e a verificação do estado do jogo:
```python
# Ajusta a saturação do frame para melhorar a detecção da imagem
frame = frameEditor.changeSaturation(frame, 1.8)

# Verifica se a câmera deve estar ativa ou não, conforme o estado do jogo
frame = frameEditor.setBlackGate(frame, truco.blackGate())
```
- <code>changeSaturation</code>: Recebe uma imagem convertida em matriz e um número flutuante, retornando a amesma alterada.
- <code>setBlackGate</code>: Recebe uma imagem convertida em matriz e uma função que retorna um booleano. Caso a função retorne True, todos os pixels da imagem são convertidos em preto.
  
Nesta fase, a imagem capturada é ajustada para facilitar a leitura das cartas pela IA. A saturação é aumentada para melhorar o contraste e a detecção. Além disso, a classe Truco determina se a câmera deve estar ativa, garantindo que o adversário não consiga ver as cartas do robô enquanto elas estão sendo analisadas.

<hr />

## Detecção de Cartas e Atualização do Estado do Jogo
O código a seguir trata da detecção das cartas nas imagens e a atualização do estado do jogo:
```python
# Detecta as cartas no frame atual
frameData = cardReader.detect(frame)

# Itera sobre os resultados da detecção
for result in frameData:
    boxes = result.boxes  # Caixas de detecção (regiões de cartas)

    # Verifica se não há cartas na tela e o buffer está cheio
    if not boxes and cardReader.cardBuffer:
        if not truco.initGame:
            truco.rollInitGame(cardReader.currentCard())
        else:
            truco.rollGame(cardReader.currentCard())

    # Desenha os retângulos de detecção e atualiza o buffer de cartas
    for box in boxes:
        frame = frameEditor.writeRectangle(frame, box)
        cardReader.cardBuffer.append(result.names[int(box.cls)])

  # Atualiza o texto a ser mostrado ao usuário
  frame = frameEditor.setWarning(frame, truco.warning)

  # Seta o momento atual do jogo no frame.
  frame = frameEditor.setActualGameLabel(frame, truco.vira, truco.myCardsWhichPlay, truco.adversaryCards)
  cv2.imshow('Truco IA Machine', frame)
  cv2.waitKey(100)
```
- <code>cardReader.detect(frame)</code>: A IA realiza a detecção das cartas presentes no frame capturado. Quando as cartas são identificadas, as informações sobre a detecção, como os nomes das cartas e os vértices das caixas de detecção, estarão armazenadas dentro das caixas de seleção, que estão dentro do resultado.
- <code>cardReader.cardBuffer</code>: Variável presente dentro de cardReader. Ela armazena uma lista com todas as deteções de cartas em um curto período de tempo, que é o período de tempo em que a pessoa levanta a carta para a câmera realizar a leitura.
- <code>truco.initGame</code>: Define se o jogo está ou não inicializado. Quando não está, significa que ele ainda está lendo cartas essenciais para que o jogo comece, tais como o vira e as cartas do robô.
- <code>truco.rollInitGame()</code>: Processa a carta que chega para ele e verifica aonde ela deve ser armazenada. Recebe a última carta detectada.
- <code>truco.rollGame()</code>: Realiza a passagem do jogo. Quando é chamado a função, ela faz o robô escolher uma carta dentre a sua mão e jogar.

Se as cartas saem de cena e o buffer está cheio, o programa processa as cartas detectadas, tomando a mediana das cartas no buffer para minimizar erros de leitura.
Dependendo do estado do jogo (initGame), a carta é processada para iniciar o jogo (caso ainda não tenha começado) ou para continuar o jogo.
Depois que as cartas são processadas, o frame e os estados de jogo são atualizados com as mensagens de alerta e rótulos de estado do jogo.

<hr />

## Fluxo do Jogo:
- Inicialização do Jogo: Se o jogo ainda não começou, a primeira carta detectada se torna o "vira". Isso é controlado pela função rollInitGame().
- Continuação do Jogo: Após a inicialização, as cartas detectadas são tratadas pela função rollGame(), que executa a lógica do jogo de truco conforme as cartas vão sendo jogadas.

<hr />

# Conclusão
Este projeto utiliza uma combinação de visão computacional e inteligência artificial para automatizar a detecção de cartas de truco, além de gerenciar o jogo de forma autônoma.
A arquitetura modular, com classes separadas para manipulação de imagens, detecção de cartas e lógica do jogo, torna o código mais organizado e fácil de expandir ou modificar.
