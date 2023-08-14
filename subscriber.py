# Example subscriber

import paho.mqtt.client as mqtt

BROKER_HOST = "broker.emqx.io"
BROKER_PORT = 1883
MQTT_TOPIC = "lora/ip"

def connection_callback(client, userdata, flags, res_code):
      if res_code == 0:
        print("Connected to broker")
        client.subscribe(MQTT_TOPIC)
      else:
        print(f"Failed to connect to broker with code: {res_code}")

def message_handler(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

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

if __name__ == "__main__":
  Subscriber(BROKER_HOST, BROKER_PORT, MQTT_TOPIC)
