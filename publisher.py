import paho.mqtt.client as mqtt
import socket
import time

BROKER_HOST = "broker.emqx.io"
BROKER_PORT = 1883
MQTT_TOPIC = "lora/ip"

# https://stackoverflow.com/questions/60656088/how-to-get-wireless-lan-adapter-wi-fi-ip-address-in-python
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1)) # doesn't have to be reachable
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


client = mqtt.Client()

def connection_callback(client, userdata, flags, res_code):
    if res_code == 0:
      print("Connected to broker")
    else:
      print(f"Failed to connect to broker with code: {res_code}")
      client.reconnect()

client.reconnect_delay_set(min_delay=5, max_delay=10)
client.on_connect = connection_callback
client.on_reconnect = connection_callback
client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_start()

while True:
  ip = get_ip_address()
  client.publish(MQTT_TOPIC, ip)
  print(f"Published `{ip}` to `{MQTT_TOPIC}` topic")
  time.sleep(5)
