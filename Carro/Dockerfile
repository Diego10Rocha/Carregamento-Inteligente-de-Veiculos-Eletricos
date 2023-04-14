# Define a imagem base que será usada
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Copia o código fonte da sua aplicação para dentro do container
COPY ./ /app

# Define o diretório de trabalho para a aplicação
WORKDIR /app

# Instala as dependências necessárias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "subscriber.py"]
#RUN python subscriber.py
# Expõe a porta que será usada pela aplicação
EXPOSE 8000

# Define o comando que será executado quando o container iniciar
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]