from flask import Flask, jsonify
import paho.mqtt.client as mqtt

BROKER_HOST = "broker.emqx.io"
BROKER_PORT = 1883
MQTT_TOPIC = "lora/ip"
IP = None

app = Flask(__name__)

def connection_callback(client, userdata, flags, res_code):
  if res_code == 0:
    print("Connected to broker")
    client.subscribe(MQTT_TOPIC)
  else:
    print(f"Failed to connect to broker with code: {res_code}")

def message_handler(client, userdata, msg):
  global IP
  IP = msg.payload.decode()
  print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
  client.disconnect()

class Subscriber:
  def __init__(self, broker, port, topic):
    self.broker = broker
    self.port = port
    self.topic = topic
    self.client = mqtt.Client()
    self.client.reconnect_delay_set(min_delay=5, max_delay=10)
    self.client.on_connect = connection_callback
    self.client.on_message = message_handler
    self.client.connect(broker, port, 60)
    self.client.loop_forever(retry_first_connection=True)

@app.route('/')
def status():
  return 'Active'

@app.route('/gateway-ip')
def gateway_ip():
  Subscriber(BROKER_HOST, BROKER_PORT, MQTT_TOPIC)
  response =  jsonify({'ip': IP })
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response
