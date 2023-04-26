FROM python:latest
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 1853/tcp
EXPOSE 1873/tcp

CMD ["python3", "main.py"]
