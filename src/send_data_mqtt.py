import time
import datetime
import paho.mqtt.client as mqtt
import ssl
import json

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

# Configuração TLS 
client.tls_set(ca_certs='/home/jhof2002/Downloads/AmazonRootCA1.pem', 
               certfile='/home/jhof2002/Downloads/****-certificate.pem.crt', 
               keyfile='/home/jhof2002/Downloads/****-private.pem.key', 
               tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)

# Conectar ao AWS IoT endpoint
client.connect("a2u5eernta1kxi-ats.iot.eu-west-2.amazonaws.com", 8883, 60)

# Iniciação do loop MQTT para manter a conexão ativa
client.loop_start()

def publishData():
    while True:
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
        value = 21.5

        # Publica a mensagem MQTT
        client.publish("raspi/data", payload=json.dumps({"timestamp": timestamp, "value": value}), qos=0, retain=False)
        print(f"Published message: {{'timestamp': '{timestamp}', 'value': {value}}}")

        # Delay
        time.sleep(5)
        

# Chamada da função para publicar dados
publishData()
