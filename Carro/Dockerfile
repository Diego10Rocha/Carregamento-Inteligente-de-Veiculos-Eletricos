# Define a imagem base que será usada
FROM python:latest

# Copia o código fonte da sua aplicação para dentro do container
COPY ./ /app

# Define o diretório de trabalho para a aplicação
WORKDIR /app

# Instala as dependências necessárias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#CMD ["python3", "Carro.py"]
#RUN python3 Carro.py
# Expõe a porta que será usada pela aplicação
EXPOSE 8889/tcp

# Define o comando que será executado quando o container iniciar
#CMD CMD ["python3", "main.py"]