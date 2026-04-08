import paho.mqtt.client as mqtt

# Broker details (use same as MQTTX)
BROKER = "127.0.0.1"      # or IP address of broker
PORT = 1883               # default MQTT port
TOPIC = "order/queue"

# Connection function
def connect_mqtt():
    global client

    client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker!")
        else:
            print("Connection failed:", rc)

    client.on_connect = on_connect

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    return client

# Publish function

def publish_message(message):
    global client

    if client is None:
        raise Exception("MQTT not connected")

    result = client.publish(TOPIC, message, retain=True)

    status = result[0]
    if status == 0:
        print("Message sent")
    else:
        print("Failed to send message")