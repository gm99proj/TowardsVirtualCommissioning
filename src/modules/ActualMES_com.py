import paho.mqtt.client as mqtt
import modules.connect_MES as MES_com
import modules.sim_ConnectMQTT as mqtt_func



# Function to handle incoming MQTT incomming messages from Plant Simulation 
def process_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message on topic {msg.topic}: {payload}")
    
    return payload

# Function to parse the incoming messages from the Plant simulation
def sim_parse_msg(payload):
    parts = payload.split(";")
    data = {}

    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            key = key.replace("#", "").strip()
            data[key] = value.strip()

    return data

# Function to communicate with the actual MES system and return the response

def order_info_publish():
    order_list = MES_com.initial_OrderMESRequest()
    mqtt_func.publish_orders(order_list)

def resource_op_publish(payload, data):
    response = MES_com.do_request(payload)

    msg_dict = MES_com.parse_message(response)

    if msg_dict:
        if msg_dict.get("ONo") == data.get("ONo") and msg_dict.get("Pos") == data.get("Pos"):
            pub_details = {
                "resource_id": int(msg_dict.get("ResourceID")),
                "operation_no": int(msg_dict.get("OpNo"))
            }

            mqtt_func.publish_operation(pub_details)

def handle_operationState(payload):
    MES_com.do_request(payload)
