# FrameEditor
Essa classe é responsável por trabalhar toda a parte de edição de um frame recebido.

## Importação
```python
import cv2
import numpy as np
```

## Explicando os métodos da classe
```python
def changeSaturation(self, frame, factor):
        imagem_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(imagem_hsv)
        s = np.clip(s * factor, 0, 255).astype(np.uint8)
        imagem_hsv_aumentada = cv2.merge([h, s, v])
        frame = cv2.cvtColor(imagem_hsv_aumentada, cv2.COLOR_HSV2BGR)
        return frame
```
Método responsável por alterar a saturação da imagem. Uma deteção de imagem via rede neural apresenta muitos fatores que podem comprometer sua legibilidade,
como iluminação, coloração, etc. A mudança de saturação é uma das implementações que estão sendo usadas para tentar melhorar a deteção.

Primeiro, é feito a conversão do frame do formado padrão BGR (não RGB) para HSV, que transforma a matriz do frame nos parâmetros Hue(matiz), 
Saturation(saturação) e Brightness(brilho). Nesse método podemos alterar esses atributos para termos uma idéia das melhores entradas para a deteção da IA.

<hr />

```python
def setBlackGate(self, frame, condition):
        if condition:
            frame[:] = 0
        return frame
```
Método que é chamado no arquivo principal do projeto, sendo responsável por ligar e desligar a visualização da câmera. 
Se o parâmetro <code>condition</code> for verdadeiro, ele seta todos os pixels da imagem como 0, se referindo ao preto.

<hr />

```python
def writeRectangle(self, frame, box):
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    frame = cv2.putText(frame, f'{box.conf[0]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0))
    return frame
```
Responsável por desenhar o quadrado na tela. É útil para verificar se a carta está sendo analisada mesmo com sem o acesso a visualização da câmera. 
Ele também mostra o nível de confiança do modelo sobre o que o mesmo está analisando.

<hr />

```python
def setWarning(self, frame, warning):
        frame = cv2.putText(frame, f'{warning}', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
        frame = cv2.putText(frame, f'{warning}', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        return frame
```
Responsável por mostrar o <code>warning</code> na tela, que é uma string que fornece informações sobre o jogo. 

<hr />

```python
 def setActualGameLabel(self, frame, vira, myCardsWhichPlay, adversaryCards):
        frame = cv2.putText(frame, f'Vira: {vira}', (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
        frame = cv2.putText(frame, f'Vira: {vira}', (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        frame = cv2.putText(frame, f'Robo: {myCardsWhichPlay}', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
        frame = cv2.putText(frame, f'Robo: {myCardsWhichPlay}', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        frame = cv2.putText(frame, f'Adversario: {adversaryCards}', (5, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 8)
        frame = cv2.putText(frame, f'Adversario: {adversaryCards}', (5, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return frame
```
Fornece ao jogador a visualização das cartas que estão sendo jogadas. A repetição do código se da para criarmos um efeito de contorno sobre os textos.
Ele fornece os dados atuais sobre o que o robô jogou de carta, o vira atual, e as cartas que o adversário está jogando.
