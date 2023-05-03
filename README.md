# MI Concorrência e Conectividade: Carregamento Inteligente de Veiculos Elétricos
O objetivo deste projeto foi a implementação de um sistema distribuído utilizando conceitos como computação em nevoa e em nuvem utilizando os protocolos de comunicação Rest e MQTT para implementar a comunicação entre as entidades do sistema que serão apresentadas no decorrer deste relatório.

## Introdução
O problema energético no mundo está se tornando cada vez mais evidente, de tal forma que nos últimos anos foram inventadas as chamadas energias limpas, estas procuram não agredir o meio ambiente e produzindo energia elétrica de forma mais eficiênte e menos poluente possível que formas tradicionais de produção de energia, tais como: energia nuclear e a energia proveniente do carvão mineral, estas formas tradicionais são conhecidas por agredirem o meio ambiente.

Além de energias limpas ou renováveis, também foram desenvolvidos outros produtos com a mesma intenção - não agredir o meio ambiente - veículos elétricos são uma destas alternativas desenvolvidas e eleitas como o futuro dos meios de transporte terrestres. Contudo carros elétricos muitas das vezes possuem autonomia limitada, logrando atenção do motorista ao conduzi-lo. Visando sanar este problema, o prefeito de uma cidade inteligente decidiu implementar um sistema IoT em sua cidade, de tal forma que motoristas de carros elétricos jamais ficariam presos devida a falta de carga nas baterias de seus respectivos veículos.

Neste relatório é apresentado um protótipo desenvolvido visando solucionar o problema supracitado, uma vez que o prefeito decidiu contratar-nos. O sistema consiste em 4 entidades, Nuvem, Névoa, Carro e Posto, estes comunicam-se por meio do protocolo de messageria MQTT bem como socket que utilizam o protocolo da camada de transporte TCP.

## Fundamentação Teórica
### MQTT
O protocolo MQTT funciona sob os princípios de publicação e assinatura, de tal forma que a sua criação deu-se devida a necessidade da indústria de petróleo e gás, uma vez que estas necessitavam de uma troca constante de informações entre suas entidades, assim desacomplando o remetente do destinatário da mensagem
O protocolo MQTT assume duas entidades:

Cliente MQTT é qualquer dispositivo capaz de executar uma biblíoteca MQTT, este é capaz de criar tópicos bem como inscrever-se em tópicos existentes. Podendo atuar como destinatário ou rementente de uma mensagem.

Agente MQTT, também conhecido como broker, este cordena as mensagens entre os diferentes clientes e responsável por receber, filtrar identificar os clientes inscritos em cada tópico e então encaminhar as mensagens aos clientes inscritos.

### Névoa
Conhecida como Névoa, a computação em borda refere-se ao processamento, armazenamento e análise dos dados mais próximos de onde eles são gerados, para que seja possvel uma reposta mais rápida, praticamente em tempo real, sendo amplamente utilizada em redes IoT e ultimamente adotada por grandes empresas de tecnologia a computação de borda, além de reduzir a latência de respostas de um recurso na internet, também é capaz de expandir a largura de banda de transmissão, garantindo um maior poder de processamento, além de reduzir a carga de tráfego de uma rede para a nuvem, uma vez que esta arquitetura no extingue a entidade nuvem, apenas a aprimora.

Atualmente a computação de borda é amplamente utilizada em Internet da Coisas e na educação, e recentemente foi utilizada em processamento de dados proveninentes da recente crise sanitária do COVID 19. Destarte atuando nos mais diversos setores da sociedade.

## Metodologia
Para solucionar o problema proposto, primeiro foram iniciados os estudos para esclarecer alguns conceitos presentes no problema como o protocolo MQTT e o que são nuvem e nevoa, como implementar uma aplicação utilizando MQTT e Socket e como criar uma imagem desse tipo de aplicação e executá-la dentro de um container docker.

A linguagem de programação escolhida para a solução do problema foi Python, apesar de que foi liberado o uso de frameworks, analisando o que o problema pede, chegou-se a conclusão de que não é necessário a utilização de nenhum.

Foi utilizado como padrão para tráfego de dados o  formato JSON(Javascript Object Notation) tanto para o envio das mensagens via MQTT quanto as requisições entre cliente e servidor socket.

Para testar as aplicações foi feito a utilização de conteiners docker e do insomnia para testar a API.
## Resultados
A solução do problema contou com uma nuvem para armazenar o melhor posto de cada região, um posto para fornecer os dados da fila, nevoas para processar e armazenar os dados das melhores filas de suas respectivas regiões e enviar para a nuvem, o carro que recebe as mensagens dos postos de sua região também processa e armazena aenas o melhor posto para quando a bateria estiver baixa ele já ter um pré processamento e só ir na nuvem caso a fila da sua região esteja muito grande.
### Nuvem
A nuvem é responsável por controlar os melhores postos de cada região. A nuvem é um servidor e irá receber de cada nevoa o melhor posto daquela região atraves de uma conexão via socket utilizando o padrão REST para se comunicar. Ao armazenar cada posto de cada região é feito o ranking dos melhores postos. A nuvem também provê um serviço via socket para que seja informado qual o melhor posto disponível baseado na fila.

### Nevoa
A nevoa é responsavel por se inscrever nos tópicos dos postos de sua região e processar qual os 3 melhores postos daquela região. A princípio há uma nevoa por região. Após processar os 3 melhores postos de sua respctiva região  a nevoa é responsável por enviar essa informação para a nuvem através de uma comunicaçãoa via socket utilizando o padrão REST.

### Posto
Os postos através do protocolo MQTT fazem publicações em tópicos de sua região passando as informações da fila e seu identificador para que a nevóa o identifique. Os tópicos que os postos fazem uma publicação "publish" são compostos por "gas_station/region/" concatenado com a região, depois vem "/id/" concatenado com o id do posto. Por exemplo um posto da região 3 com id "6fd2561f-f70c-448e-8b63-49e41b52e14f" o tópico de publish seria "gas_station/region/3/id/6fd2561f-f70c-448e-8b63-49e41b52e14f".

### Carro
No carro há um servidor para tratar as requisições de uma API Rest para informar o status atual do carro que informa o nível da bateria caso esteja acima de 30%, caso contrário é informado qual o posto e qual a região que possui melhor fila para abastecimento.
Há também um cliente que se inscreve nos tópicos dos postos de sua região para processar o melhor posto daquela região e deixar armazenado. É feito também o gerenciamento da bateria, então quando a bateria está abaixo de 30% é verificado qual o melhor posto daquela região, caso o melhor posto tenha mais de 10  carros na fila é feita uma consulta na nuvem para saber se há algum posto em outra região com fila ao menos 30% menor que o melhor posto da região que o carro está localizado, após fazer os calculos um posto é escolhido e o carro é direcionado a ele para fazer a recarga da bateria.

### Docker
Foi criado uma imagem docker para cada aplicação apresentada acima e estas imagens foram disponibilizadas no repositório online do docker hub. Para poder ter estas aplicações executando em um computador basta alterar o nome da imagem para o nome correspondente no dockerhub no arquivo docker-compose.yml, após isso basta abrir no terminal a pasta raiz do sistema desejado e executar o seguinte comando:


```
$ docker compose up
```

É importante ressaltar que a nuvem deve ser configurada na maquina com IP: ```172.16.103.7```. Deve ser configurado 3 nevoas nas maquinas de seguinte IP: ```172.16.103.3```, ```172.16.103.5```, ```172.16.103.8```.

O repositório do dockerhub está no link: <a>https://hub.docker.com/repository/docker/diego10rocha/pbl2_redes/general</a>. E as imagens utilizadas foram:
- Nuvem: diego10rocha/pbl2_redes:nuvem_final
- Nevoa: diego10rocha/pbl2_redes:nevoa
- Posto: diego10rocha/pbl2_redes:posto_random
- Carro: diego10rocha/pbl2_redes:carro_random

Entretanto, vale ressaltar que apenas a nevoa não é inicializado junto ao container, para executa-la é necessário abrir o terminal do container e executar o comando:

```
$ python3 main.py
```

É necessário também ter uma imagem de um broker funcionando, para instalar basta fazer o pull da seguinte imagem:

```
$ docker pull eclipse-mosquitto
```
Após instalar a imagem do broker é necessário rodar fazendo as devidas configurações que podem ser feitas atraves do terminal executando o seguinte comando:
```
$ docker run -it -p 1883:1883 -p 1017:1017 -v mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```
Visto que "1017:1017" é um exemplo de porta para o broker, entretanto o sistema está configurado para funcionar nas seguintes portas e ips de acordo com cada região:
- Região 1: 
    - IP: 172.16.103.3
    - Porta: 1017
- Região 2:
    - IP: 172.16.103.5
    - Porta: 8331
- Região 3:
    - IP: 172.16.103.8
    - Porta: 1888

Então uma imagem docker do brocker deve ser configurada em cada uma das respctivas maquinas identificadas pelo devido IP.
## Conclusão

Os sistemas desenvolvidos resolvem o problema proposto, entretanto há formas melhores de resolver o problema principalmente pensando no quesito de escalabilidade de sistemas. No sistema desenvolvido o carro recebe mensagens diretamente dos postos das regiões, entretante como a nevoa já faz um processamento de qual o melhor posto da respectiva região, uma alternativa a esta solução pensando em um desempenho melhor seria fazer com que a nevoa enviasse aos carros da sua região qual o melhor posto, eviando que cada carro processe a mesma informação e sobrecarregue o servidor MQTT responsável pela publicação de mensagens dos postos. Importante falar também que foi utilizado JSON para padronizar as mensagens trocadas via MQTT e nas requisições cliente-servidor via socket.
