# Truco IA Machine
Este projeto utiliza visão computacional para detectar cartas de truco em tempo real por meio de uma webcam. Ele é responsável por detectar as cartas e gerenciar o estado do jogo de truco automaticamente.

## Instalação e inicialização:

1. Clone o repositório do projeto.
2. Instale as dependências necessárias executando o comando:
```bash
pip install opencv-python ultralytics logging statistics
```
3. Rode os seguintes comandos:
```bash
cd truco-ia-machine
python truco-ia-machine.py
```

# Leitura da carta
Uma das principais diferenças do robô é a capacidade dele jogar com um baralho físico, por meio de visão computacional. O sistema utiliza o YOLOv8 para realizar o processamento de predição das cartas na câmera. Como não é um processo 100% certeiro, habilitei um sistema para carregar um buffer de vários frames seguidos. Esse buffer não tem uma quantidade máxima de elementos, mas possui uma quantidade mínima, suficiente para que o sistema possa ter mais confiança quanto, sem querer, o usuário passe alguma carta sem querer na frente da câmera.

# Processo inicial do jogo:
- Para começar o jogo, rode o script <code>truco-ia-machine.py</code>. É necessário que você tenha uma câmera para que o jogo funcione. Rodando o script, será aberto uma janela na tela do computador.
- Após a abertura, o usuário deve mostrar, na câmera do computador, a carta do baralho que receberá a função de "Vira". Essa carta serve para modificar a ordem de poder do baralho. de forma que, alinhando as cartas por poder, caso o vira seja i, a carta de maior poder será i+1, ou seja, a carta seguinte ao vira no nível de poder.
- A janela então ficará inteira preta, sendo somente possível ler os textos e as caixas sinalizando a leitura de uma carta. Enquanto a janela estiver preta, o usuário irá setar as cartas do robô, de modo que não consiga ver qual carta é pela câmera.

# Durante o jogo:
Na primeira etapa, o jogo poderá começar de 4 formas, sendo elas:
- O usuário começa e joga uma carta;
- O usuário começa e pede truco;
- O robô começa e joga uma carta;
- O robô começa e pede truco;

*A chance de você ou o robô começar é de 50% para ambos.*

Como o código segue um padrão de ações reativas, as ações do robô são realizadas a partir da ação do próprio usuário, ou seja, toda vez que o usuário mostrar uma carta ou pressionar uma das teclas de função do programa, o robô irá realizar alguma ação. Desse modo, podemos dizer que, quando o robô começa, significa que ele já fez uma ação a partir do momento que você mostrou a última carta da mão dele. Ele verificará, depois de adicionar a carta em sua mão, se ele já está com a mão completa. Caso sim, irá verificar randomicamente quem começa, e se caso ele começar, já jogará uma carta.
Caso o robô começe, o usuário jogará a última carta, e vise-versa.

# Truco:
O truco é um processo que acontece dentro do esquema apresentado anteriormente. Tanto o robô quanto o usuário podem pedir truco a qualquer momento, desde que estejam na sua vez de jogar. Não é possível pedir truco após jogar uma carta. Caso o robô esteja começando, antes de jogar a carta, ele irá verificar, em uma certa probabilidade, se pedirá truco ou não. Caso peça, o mesmo irá travar a execução do passo de jogar a carta, passo esse que então será realizado caso o jogador aceite o truco.

### Caso o robô peça truco, ele interrompirá o processo de jogar a carta, e então terá 3 possibilidades:
- Caso o usuário aceite o truco, o mesmo irá jogar a carta que ele iria jogar.
- Caso o usuário rejeite, será contabilizado um ponto para o robô.
- Caso o usuário dobre, o robô irá entrar no mesmo processo de escolha do truco novamente. Será semelhante ao processo do usuário pedir o truco.

### Caso o usuário peça truco, será chamada uma função para o robô decidir o que ele fará, e a resposta do mesmo terá 3 possibilidades:
- O robô pode aceitar o truco, fazendo que a partida comece a valer mais pontos.
- O robô pode rejeitar o truco, fazendo com que o usuário ganhe um ponto a mais automaticamente.
- O robô pode dobrar a aposta, fazendo com que o usuário tenha que responder com a tecla de teclado se aceita ou não.

### Fatos adicionais:
- O período do truco deve acabar a partir do momento em que for jogada a última carta da rodada.

# Empache
No truco, o naipe é valido para verificar o poder de uma certa carta. No caso do vira, os 4 naipes da carta subsequente dele serão as mais poderosas do jogo, seguindo a ordem de poder dos naipes. Para as outras cartas, irá ser apresentado o conceito de empache. O empache acontece quando, na primeira partida, as duas maiores cartas da rodada são a mesma carta com o naipe diferente. Após isso acontecer, os jogaodores devem mostrar suas maiores cartas. Antes da pessoa jogar sua carta, ela também pode pedir truco, aumentando a aposta antes de revelar sua carta. Vencerá aquele que jogar a maior carta, e, se essas cartas mais fortes entre 2 adversários forem a mesma, com o mesmo naipe, aí então se considerará o naipe delas.

No caso de empache na segunda ou terceira rodada, ganhará o time ou jogador que tiver ganhado a primeira rodada.




