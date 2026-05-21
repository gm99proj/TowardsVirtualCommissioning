import paho.mqtt.client as mqtt
from modules.MES_com import on_message


# Broker details (use same as MQTTX)
BROKER = "127.0.0.1"      # or IP address of broker
PORT = 1883               # default MQTT port
TOPIC = "order/queue"
TOPIC_Sub = [("workplan/plan", 0), ("order/operation/state", 0)]

client = None

# Connection function
def connect_mqtt():
    global client

    client = mqtt.Client(userdata={
        "order_com": None,
        "mes_com": None
    })

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker!")
            client.subscribe(TOPIC_Sub) # Subscribe to both topics
        else:
            print("Connection failed:", rc)

    client.on_connect = on_connect
    client.on_message = on_message

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


