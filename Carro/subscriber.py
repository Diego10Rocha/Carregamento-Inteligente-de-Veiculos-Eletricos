import random
import threading
import time

from paho.mqtt import client as mqtt_client

BROKER = 'localhost'

broker = BROKER
port = 1883
topic = "posto/id/#"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
BATTERY_TOTAL_CHARGE = 10
BATTERY_LEVEL = BATTERY_TOTAL_CHARGE


# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def mqtt_connect():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

def battery_manager(batery_level):
    while(batery_level != 0):
        time.sleep(1)
        batery_level = batery_level - 1

        if(batery_level < BATTERY_TOTAL_CHARGE * 0.3):
            print("Bateria descarregada")
            #Escolher posto
    print("O carro morreu, impossível ir até um posto")

if __name__ == '__main__':
    t1 = threading.Thread(target=mqtt_connect)

    t2 = threading.Thread(target=battery_manager(BATTERY_LEVEL))
    #mqtt_connect()

    # iniciar a thread do mqtt
    t1.start()

    # iniciar a thread de gerenciamento da bateria
    t2.start()

