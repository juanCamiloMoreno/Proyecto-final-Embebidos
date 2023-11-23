import socket
import time
import board
import adafruit_ltr390
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt
import json
from datetime import datetime
from w1thermsensor import W1ThermSensor
import queue
from queue import Queue
from threading import Thread
import csv

# Datos de tu dispositivo y acceso MQTT
THINGSBOARD_HOST = "thingsboard.cloud"
ACCESS_TOKEN = "mobmzp9wjqylrk29bj8h"

# Tema MQTT para enviar datos
MQTT_TOPIC = "v1/devices/me/telemetry"

# Busca autom      ticamente el sensor DS18B20 conectado
sensor = W1ThermSensor()
#Busca automaticamente el sensor LTR390
i2c = board.I2C()
ltr = adafruit_ltr390.LTR390(i2c)

cola_temperatura =queue.LifoQueue()
cola_UV = queue.LifoQueue()
cola_timestap = queue.LifoQueue()

# Bandera para controlar si el cliente MQTT está conectado
mqtt_conectado = False

def on_connect(client, userdata, flags, rc):
    global mqtt_conectado
    if rc == 0:
        print("Conexión exitosa con el servidor MQTT")
        mqtt_conectado = True
    else:
        print(f"Fallo en la conexión con código de retorno: {rc}")

def on_disconnect(client, userdata, rc):
    global mqtt_conectado
    print("Desconectado del servidor MQTT")
    mqtt_conectado = False

def conectar_mqtt():
    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    try:
        client.connect(THINGSBOARD_HOST, 1883, 60)
        client.loop_start()  # Iniciar el bucle de eventos MQTT
    except Exception as e:
        print(f"Fallo en la conexión: {e}")

    return client

def leer_datos_sensores():
    global cola_temperatura
    global cola_UV
    global cola_timestap
    UV=ltr.uvs
    cola_UV.put(UV)
    temperature = sensor.get_temperature()
    cola_temperatura.put(temperature)
    timestap = datetime.now().isoformat()
    cola_timestap.put(timestap)
    print("Leyendo sensores")

def nube(client):
    global cola_temperatura
    global cola_UV
    global cola_timestap
    while not cola_temperatura.empty():
        if mqtt_conectado:
            temperatura = cola_temperatura.get()
            irradiancia = cola_UV.get()
            timestap = cola_timestap.get()
            # Crear un diccionario JSON con los datos y el timestamp en formato ISO 8601
            data = {
                "temperature": temperatura,
                "irradiance": irradiancia,
                "ts": timestap  # Agregar el timestamp en formato ISO 8601
            }
            try:
                client.publish(MQTT_TOPIC, json.dumps(data), 1)
                print("Enviando datos")
                time.sleep(1)
            except Exception as e:
                print(f"Fallo al enviar datos: {e}")
        else:
             client.reconnect()

# Funci      n para guardar datos en un archivo CSV
def guardar_en_csv():
    global cola_temperatura
    global cola_UV
    global cola_timestap
    timestamp = cola_timestap.get()
    temperatura = cola_temperatura.get()
    irradiancia = cola_UV.get()
    with open("datos_sensores.csv", "a", newline="") as csvfile:
        fieldnames = ["timestamp", "Temperatura", "UV"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()  # Escribir encabezados solo si el archivo est       vac      o
        writer.writerow({"timestamp": timestamp, "Temperatura": temperatura, "UV": irradiancia})
    cola_UV.put(irradiancia)
    cola_temperatura.put(temperatura)
    cola_timestap.put(timestamp)

def check_internet_connection():
    try:
        # Intenta establecer una conexión con un servidor externo
        socket.create_connection(("www.google.com", 80))
        print("si hay conexion")
        return True
    except OSError:
        pass
    return False

def main():
    client = conectar_mqtt()

    while True:
        try:
            leer_datos_sensores()
            if check_internet_connection():               
               nube(client)
            else:
               guardar_en_csv()
            
            time.sleep(4)
        except KeyboardInterrupt:
            print("Interrupcion de teclado detectada. El script se detiene.")
            client.disconnect()
            print("Programa detenido por el usuario.")
            break
        
    
if __name__ == "__main__":
    main()
