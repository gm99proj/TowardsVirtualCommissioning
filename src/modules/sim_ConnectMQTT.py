import paho.mqtt.client as mqtt
import modules.ActualMES_com as mes_com
import json
import modules.mes_interface as mes

# Broker details (use same as MQTTX)
BROKER = "127.0.0.1"      # or IP address of broker
PORT = 1883               # default MQTT port
TOPIC = "workplan/plan"

client = None

def client_setup():

    global client
    client = mqtt.Client()
    
    def sim_on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(TOPIC)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_disconnect(client, userdata, rc):
        print("Disconnected from MQTT Broker with code:", rc)

    client.on_connect = sim_on_connect
    client.on_disconnect = on_disconnect
    client.on_message = sort_request

    try:
        client.connect(BROKER, PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"MQTT connection failed: {e}")
    
    return client


def sim_data(msg):
    payload = mes_com.process_message(client, None, msg)
    return payload

def sort_request(client, userdata, msg):
    try:
        payload = sim_data(msg)

        data = mes_com.sim_parse_msg(payload)

        if data.get("MClass") == 101:
            mes_com.handle_operationState(payload)
        else:
            mes_com.resource_op_publish(payload, data)
    
    except Exception as e:
        print("Error handling message:", e)

def publish_orders(orders):
    """Publish all discovered orders to MQTT.

    Topics:
        mes4/orders/list         <- full list of all orders+positions as JSON
    """

    if client is None:
        print("MQTT not connected")
        return
    
    if not orders:
        print("No orders to publish")
        return

    all_positions = [pos for positions in orders.values() for pos in positions]

    # Publish full list
    topic = f"{mes.MQTT_TOPIC_BASE}/list"
    payload = json.dumps(all_positions)
    client.publish(topic, payload)

    print_payload = json.dumps(all_positions, indent=2)
    #print(f"Published to {topic}:\n{print_payload}")

def publish_operation(details):
    """Publish operation details to MQTT.

    Topics:
        mes4/orders/operation   <- details of a resource operation as JSON
    """
    if client is None:
        print("MQTT not connected")
        return
    
    if not details:
        print("No operation details to publish")
        return

    topic = f"{mes.MQTT_TOPIC_SIM}/operation"
    payload = json.dumps(details)
    client.publish(topic, payload)

    print_payload = json.dumps(details, indent=2)
    #print(f"Published to {topic}:\n{print_payload}")