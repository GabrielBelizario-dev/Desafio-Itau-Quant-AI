# Desafio-Itau-Quant-AI

26/08/2025:
Hoje é o dia da primeira live institucional.
Buscando um modelo matemático inicial, encontrei o Processo Ornstein-Uhlenbeck(OU), um modelo robusto e amplamente utilizado para modelar a reversão à média. Este processo descreve a evolução de uma variável que é puxada para sua média de longo prazo com uma certa "força".
A equação diferencia para o processo OU é:

dYt = θ(μ−Yt)dt + σdWt, Onde:

Yt é o preço do ativo no tempo;
θ é a velocidade de reversão;
μ é o nível de reversão à média;
σ é a volatilidade do processo;
dWt é o termo de ruído aleatório, representando um movimento browniano.

Indo mais a fundo, encontrei novos modelos, mais robustos. 
Em especial, dois modelos de Séries Temporais me chamaram atenção:
ARIMA (Autoregressive Integrated Moving Average) que em essência modela a relação entre valores atuais e passados de uma série;
GARCH (Generalized Autoregressive Conditional Heteroskedasticity) que não se concentra em prever o preço ou o retorno em si, mas a volatilidade. 
Percebi uma certa complementação entre os dois modelos e talvez aplicá-los conjuntamente seja uma ótima opção.

