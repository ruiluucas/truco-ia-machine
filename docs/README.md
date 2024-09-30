# Truco IA Machine
Este projeto utiliza visão computacional para detectar cartas de truco em tempo real por meio de uma webcam. Ele é responsável por detectar as cartas e gerenciar o estado do jogo de truco automaticamente.

# Sumário
- [Instalação e inicialização](#Instalação-e-inicialização);
- [Processo inicial do jogo](#Processo-inicial-do-jogo);
- [Processamento de leitura da carta](#Processamento-de-leitura-da-carta);
- [Processo durante o jogo](#Processo-durante-o-jogo);
- [Pedir truco](#Pedir-truco);
- [Empache](#Empache);
- [Histórias de usuário](#Histórias-de-usuário)
- [Casos de uso](#Casos-de-uso)

# Instalação e inicialização:
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

# Processo inicial do jogo:
- Para começar o jogo, rode o script <code>truco-ia-machine.py</code>. É necessário que você tenha uma câmera para que o jogo funcione. Rodando o script, será aberto uma janela na tela do computador.
- Após a abertura, o usuário deve mostrar, na câmera do computador, a carta do baralho que receberá a função de "Vira". Essa carta serve para modificar a ordem de poder do baralho. de forma que, alinhando as cartas por poder, caso o vira seja i, a carta de maior poder será i+1, ou seja, a carta seguinte ao vira no nível de poder.
- A janela então ficará inteira preta, sendo somente possível ler os textos e as caixas sinalizando a leitura de uma carta. Enquanto a janela estiver preta, o usuário irá setar as cartas do robô, de modo que não consiga ver qual carta é pela câmera.

# Processamento de leitura da carta
Uma das principais diferenças do robô é a capacidade dele jogar com um baralho físico, por meio de visão computacional. O sistema utiliza o YOLOv8 para realizar o processamento de predição das cartas na câmera. Como não é um processo 100% certeiro, habilitei um sistema para carregar um buffer de vários frames seguidos. Esse buffer não tem uma quantidade máxima de elementos, mas possui uma quantidade mínima, suficiente para que o sistema possa ter mais confiança quando, sem querer, o usuário mostre alguma carta sem querer na frente da câmera.

Após o jogador disponibilizar a quantidade mínima de frames ao robô, caso ele tire a carta da frente da câmera, o jogo irá seguir por dois caminhos padrões: <code>rollInitGame</code> e <code>rollGame</code>. A primeira função é responsável por setar toda a parte inicial do jogo, como adicionar o vira e as cartas do robô na memória.

# Processo durante o jogo:
Na primeira etapa, o jogo poderá começar de 4 formas, sendo elas:
- O usuário começa e joga uma carta;
- O usuário começa e pede truco;
- O robô começa e joga uma carta;
- O robô começa e pede truco;

*A chance de você ou o robô começar é de 50% para ambos.*

Como o código segue um padrão de ações reativas, as ações do robô são realizadas a partir da ação do próprio usuário, ou seja, toda vez que o usuário mostrar uma carta ou pressionar uma das teclas de função do programa, o robô irá realizar alguma ação. Desse modo, podemos dizer que, quando o robô começa, significa que ele já fez uma ação a partir do momento que você mostrou a última carta da mão dele. Ele verificará, depois de adicionar a carta em sua mão, se ele já está com a mão completa. Caso sim, irá verificar randomicamente quem começa, e se caso ele começar, já jogará uma carta.
Caso o robô começe, o usuário jogará a última carta, e vise-versa.

# Pedir truco:
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

# Histórias de usuário
Aqui se encontram alguns requisitos que já foram pensados para o programa, para facilitarmos a análise dos requisitos para a construção do programa.

| Id | História de usuário |
| --- | --- |
| HU01 | Como jogador, quero mostrar para ao robô suas respectivas cartas, para que ele guarde em memória e saiba o que ele pode jogar na mesa |
| HU02 |  Como jogador, quero mostrar a carta vira ao robô para que ele indentifique a carta mais forte do jogo naquela rodada com base nela |
| HU03 |  Como jogador, quero que o robô saiba qual carta eu joguei naquele determinado momento, para que ele possa tomar a decição de qual carta ele deve jogar posteriormente |
| HU04 |  Como jogador, quero ter a possibilidade de pedir truco, para que o valor da partida atual aumente |
| HU05 |  Como jogador, quero poder escolher se aceito o truco vindo do robô, para que eu não saia prejudicado caso minha mão esteja ruim |
| HU06 | Como jogador, quero poder empachar a carta para que a próxima jogada seja mostrar a carta mais forte |

# Casos de uso
Aqui se encontra o fluxograma de algumas funções de chamada do projeto. As funções contidas no fluxograma representam uma visão mais funcional acerca do código que ela explica. Quando uma função A estiver apontando com a flecha para uma função B, e essa mesma flecha ter o nome ``<<include>>``, significa que a função A irá chamar obrigatóriamente a função B toda vez que for ativada. No entanto, caso a função A esteja recebendo uma flecha da função B, e essa flecha ter o nome  ``<<extend>>``, significa que a função A não irá chamar a função B sempre, dependendo de algumas circunstâncias de lógica para que isso aconteça.

Acesse o fluxograma por esse link [aqui!](https://www.figma.com/board/gaVoQwrtfulGMpGzptF5oi/truco-ia-machine%2Fuse-cases?node-id=0-1&t=nu9bwybsKcnxly5I-1)

<table>
  <tr>
    <th colspan="2"><h2>Mostrar vira</h2></th>
  </tr>
  <tr>
    <th>Ator principal</th>
    <td>Usuário</td>
  </tr>
  <tr>
    <th>Ator secundário</th>
    <td>Sistema</td>
  </tr>
  <tr>
    <th>Resumo</th>
    <td>Descreve a adição do vira na partida</td>
  </tr>
  <tr>
    <th>Pré condição</th>
    <td>Usuário ter mostrado a carta ao robô no momento em que o mesmo está apto a ler a carta "vira"</td>
  </tr>
  <tr>
    <th>Pós condição</th>
    <td>Vira adicionado, ordem de poder das cartas alterada de acordo com o vira, tela fica preta e as próximas 3 cartas a serem jogadas serão transferidas para a mão do robô</td>
  </tr>
  <tr>
    <th colspan="2">Fluxo normal</th>
  </tr>
  <tr>
    <th>Ator principal</th>
    <th>Sistema</th>
  </tr>
  <tr>
    <td></td>
    <td>Robô fica em modo reativo para a próxima carta analisada se tornar o vira</td>
  </tr>
  <tr>
    <td>Usuário mostra a carta ao robô</td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>Robô analisa o poder da carta</td>
  </tr>
  <tr>
    <td></td>
    <td>Robô troca toda a ordem de poder das cartas para que o vira seja a mais forte</td>
  </tr>
  <tr>
    <td></td>
    <td>Robô escurece a tela para que o jogador não possa ver as próximas cartas a serem analisadas pelo robô</td>
  </tr>
   </tr>
  <tr>
    <th colspan="2">Fluxo alternativo</th>
  </tr>
  <tr>
    <td colspan="2">Usuário lança uma carta que não está entre as cartas utilizadas no truco</td>
  </tr>
  <tr>
</table>

<table>
  <tr>
    <th colspan="2"><h2>Verificar cartas do robô</h2></th>
  </tr>
  <tr>
    <th>Ator principal</th>
    <td>Usuário</td>
  </tr>
  <tr>
    <th>Ator secundário</th>
    <td>Sistema</td>
  </tr>
  <tr>
    <th>Resumo</th>
    <td>Adiciona as 3 cartas referentes ao robô na partida</td>
  </tr>
  <tr>
    <th>Pré condição</th>
    <td>Usuário ter mostrado a carta ao robô no momento em que o mesmo está apto a ler as 3 cartas; Já ter lido o vira;</td>
  </tr>
  <tr>
    <th>Pós condição</th>
    <td>Vira adicionado, ordem de poder das cartas alterada de acordo com o vira, tela fica preta e as próximas 3 cartas a serem jogadas serão transferidas para a mão do robô</td>
  </tr>
  <tr>
    <th colspan="2">Fluxo normal</th>
  </tr>
  <tr>
    <th>Ator principal</th>
    <th>Sistema</th>
  </tr>
  <tr>
    <td></td>
    <td>Robô fica em modo reativo para ler as 3 cartas</td>
  </tr>
  <tr>
    <td>Usuário mostra a carta ao robô</td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>Robô adiciona a carta a mão</td>
  </tr>
  <tr>
    <td>Usuário mostra a carta ao robô</td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>Robô adiciona a carta a mão</td>
  </tr>
  <tr>
    <td>Usuário mostra a carta ao robô</td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>Robô adiciona a carta a mão</td>
  </tr>
  <tr>
    <td></td>
    <td>Robõ verifica que foram adicionadas as 3 cartas</td>
  </tr>
  <tr>
    <td></td>
    <td>Robõ verifica quem começa entre ele e o jogador.</td>
  </tr>
  <tr>
    <td></td>
    <td>Quando o robô começa, o mesmo seta a probabilidade de chamar truco com base em suas cartas. Caso decida não trucar, termina</td>
  </tr>
  <tr>
    <td></td>
    <td>Sistema reabilita a tela do jogo.</td>
  </tr>
  <tr>
    <th colspan="2">Fluxo alternativo</th>
  </tr>
  <tr>
    <td colspan="2">Jogador lança uma carta repetida</td>
  </tr>
   <tr>
    <td colspan="2">Usuário começa, fazendo com que o robô não jogue nada no começo./td>
  </tr>
  <tr>
    <td colspan="2">Robô começa e pede truco logo antes de jogar qualquer carta./td>
  </tr>
  <tr>
</table>




