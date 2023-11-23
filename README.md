
# Projecto Final Embebidos

# README

Este README proporciona una descripción básica del código y su funcionalidad, así como información sobre cómo configurar y ejecutar el script.

## Descripción

Este script en Python se diseñó para leer datos de sensores de temperatura (DS18B20) y radiación ultravioleta (LTR390), y enviar estos datos a un servidor MQTT en ThingsBoard. Si no hay conexión a Internet, los datos se guardan localmente en un archivo CSV.

## Requisitos

- Python 3.x instalado en el sistema.
- Bibliotecas Python: `adafruit-circuitpython-ltr390`, `Adafruit-Blinka`, `w1thermsensor`, `paho-mqtt`, `board`.
- Acceso a un servidor MQTT (en este caso, se utiliza ThingsBoard).

## Configuración

Antes de ejecutar el script, asegúrate de realizar las siguientes configuraciones:

1. **Datos de acceso MQTT:** Reemplaza los valores de `THINGSBOARD_HOST` y `ACCESS_TOKEN` con los correspondientes a tu instancia de ThingsBoard.

```python
THINGSBOARD_HOST = "thingsboard.cloud"
ACCESS_TOKEN = "mobmzp9wjqylrk29bj8h"
```

2. **Tema MQTT:** Puedes personalizar el tema MQTT según tus necesidades.

```python
MQTT_TOPIC = "v1/devices/me/telemetry"
```

3. **Datos del sensor DS18B20:** Asegúrate de que el sensor DS18B20 esté conectado y configurado automáticamente.

```python
sensor = W1ThermSensor()
```

4. **Datos del sensor LTR390:** Asegúrate de que el sensor LTR390 esté conectado y configurado automáticamente.

```python
i2c = board.I2C()
ltr = adafruit_ltr390.LTR390(i2c)
```

## Ejecución

1. Ejecuta el script desde la línea de comandos:

```bash
python nombre_del_script.py
```

2. El script leerá continuamente los datos de los sensores, intentará enviarlos al servidor MQTT y guardará localmente si no hay conexión a Internet.

3. Para detener el script, presiona `Ctrl + C` en la línea de comandos.

## Notas

- Asegúrate de tener una conexión a Internet activa para enviar datos a ThingsBoard.
- Los datos se envían cada 10 segundos, según el valor de `time.sleep(10)` en la función principal.
- Los datos se guardan en un archivo CSV llamado "datos_sensores.csv" en caso de falta de conexión a Internet.

Este README proporciona instrucciones básicas. Asegúrate de revisar el código para comprender completamente su funcionamiento y realizar cualquier ajuste necesario para adaptarlo a tus requisitos específicos.