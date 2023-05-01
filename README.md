# MI Concorrência e Conectividade: Carregamento Inteligente de Veiculos Elétricos
O objetivo deste projeto foi a implementação de um sistema distribuído utilizando conceitos como computação em nevoa e em nuvem utilizando os protocolos de comunicação Rest e MQTT para implementar a comunicação entre as entidades do sistema que serão apresentadas no decorrer deste relatório.

## Introdução

## Fundamentação Teórica

## Metodologia

## Resultados

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

O repositório do dockerhub está no link: <a>https://hub.docker.com/repository/docker/diego10rocha/pbl2_redes/general</a>. E as imagens utilizadas foram:
- Nuvem: diego10rocha/pbl2_redes:nuvem_final
- Nevoa: diego10rocha/pbl2_redes:nevoa
- Posto: diego10rocha/pbl2_redes:posto_random
- Carro: diego10rocha/pbl2_redes:carro_random

Entretanto, vale ressaltar que apenas a nevoa não é inicializado junto ao container, para executa-la é necessário abrir o terminal do container e executar o comando:

```
$ python3 main.py
```


## Conclusão