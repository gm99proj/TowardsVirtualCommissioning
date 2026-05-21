import paho.mqtt.client as mqtt
import xml.etree.ElementTree as ET
import pandas as pd
import json

# Load the temperary database acts as MES
xls_file = "src/database/order_state.xlsx"
xml_file = "src/database/workplan_database.xml"

# Setup MQTT connection parameters
# BROKER = "127.0.0.1"
# PORT = 1883
# TOPIC = [("workplan/plan", 0), ("order/operation/state", 0)]

mes_db = ET.parse(xml_file)
root = mes_db.getroot()  

# Function to parse the incoming messages from the Plant simulation
def parse_msg(payload):
    parts = payload.split(";")
    data = {}

    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            key = key.replace("#", "").strip()
            data[key] = value.strip()

    return data

# Function to handle incoming MQTT messages for MES communication and order state updates

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message on topic {msg.topic}: {payload}")
    
    data = parse_msg(payload)

    if msg.topic == "order/operation/state":
        userdata["order_com"] = data

    elif msg.topic == "workplan/plan":
        userdata["mes_com"] = data

    # Only process when BOTH exist
    if userdata["order_com"] and userdata["mes_com"]:
        order_df = load_order_state()

        handle_mes_request(
            userdata["order_com"],
            userdata["mes_com"],
            load_order_state(),
            client
        )

        # IMPORTANT: reset after processing
        userdata["order_com"] = None
        userdata["mes_com"] = None


# Functions to check the order in the excel database
def load_order_state():
    order_df = pd.read_excel(xls_file)
    return order_df

# Function to get the workplan details based on the incoming MES communication
def MES_com(order_com, planID): 
    for workplan in root.findall("workplan"):
        if workplan.get("id") == order_com.get("WorkplanNo"):
            for plan in workplan.findall("plan"):
                if plan.get("row") == str(planID):
                    plan_dict = {
                        "stepNo": plan.findtext("stepNo"),
                        "operation": plan.findtext("operation"),
                        "resource": plan.findtext("resource"),
                        "nextStep": plan.findtext("nextStep"),
                        "description": plan.findtext("description"),
                    }
                    return plan_dict
    return None

#Function to handle the incomming the MES requests and update the order state in the excel database
def handle_mes_request(order_com, mes_com, order_df,client):
    m_class = mes_com.get("MClass")
    m_no = mes_com.get("MNo")
    request_ID = mes_com.get("RequestId")

    # Get First operation for the resource and return the details to the Plant simulation
    if m_class == "100" and m_no == "4":
        planID = 1
        MES_info = MES_com(order_com, planID)
        order_details = {
            "order_no": order_com.get("OrderNo"),
            "order_pos": order_com.get("OrderPos"),
            "resource_id": MES_info.get("resource"),
            "operation_no": MES_info.get("operation"),
            "description": MES_info.get("description"),
            "step_no": MES_info.get("stepNo"),
            "sim_location": order_com.get("StationName"),
            "assignment": order_com.get("PalletID"),
            "status": "Assigned"
        }
        pub_details = {
            "resource_id": int(MES_info.get("resource")),
            "operation_no": int(MES_info.get("operation"))
        }
        pub_details_json = json.dumps(pub_details)
        order_df = pd.concat([order_df, pd.DataFrame([order_details])], ignore_index=True)
        client.publish("workplan/plan/set", pub_details_json)
        order_df.to_excel(xls_file, index=False)

    # Get the next operation for the resource and return the details to the Plant simulation
    elif m_class == "100" and m_no == "6":
        o_no = int(mes_com.get("ONo"))
        o_pos = int(mes_com.get("OPos"))
        pallet_id = int(order_com.get("PalletID"))
        count = count_order_in_df(o_no, o_pos, pallet_id, order_df)
        planID = count + 1
        MES_info = MES_com(order_com, planID)
        order_details = {
            "order_no": mes_com.get("ONo"),
            "order_pos": mes_com.get("OPos"),
            "resource_id": MES_info.get("resource"),
            "operation_no": MES_info.get("operation"),
            "description": MES_info.get("description"),
            "step_no": MES_info.get("stepNo"),
            "sim_location": order_com.get("StationName"),
            "assignment": order_com.get("PalletID"),
            "status": "Assigned"
        }
        pub_details = {
            "resource_id": int(MES_info.get("resource")),
            "operation_no": int(MES_info.get("operation"))
        }
        pub_details_json = json.dumps(pub_details)
        order_df = pd.concat([order_df, pd.DataFrame([order_details])], ignore_index=True)
        client.publish("workplan/plan/set", pub_details_json)
        order_df.to_excel(xls_file, index=False)

    # Start the operation and update the order state to "In Progress" in the excel database
    elif m_class == "101" and m_no == "10":
        o_no = int(mes_com.get("ONo"))
        o_pos = int(mes_com.get("OPos"))
        resource_id = int(order_com.get("ResourceID"))
        order_df.loc[(order_df["order_no"] == o_no) & (order_df["order_pos"] == o_pos) & (order_df["resource_id"] == resource_id), "status"] = "In Progress"
        order_df.to_excel(xls_file, index=False)
        if (order_df["status"] == "In Progress").any():
            pub_order_details ={
            "resource_id": resource_id,
            "Status": "In Progress"
        }
            pub_order_details_json = json.dumps(pub_order_details)
            client.publish("order/operation/state/set", pub_order_details_json)
        else:
            print("Something went wrong when updating the order state to In Progress.")
    
    #Set the order state to "Completed" when the operation is completed and update the excel database
    elif m_class == "101" and m_no == "20":
        o_no = int(mes_com.get("ONo"))
        o_pos = int(mes_com.get("OPos"))
        pallet_id = int(mes_com.get("CarrierID"))
        resource_id = int(order_com.get("ResourceID")) 
        order_df.loc[(order_df["order_no"] == o_no) & (order_df["order_pos"] == o_pos) & (order_df["resource_id"] == resource_id) & (order_df["assignment"] == pallet_id), "status"] = "Completed"
        order_df.to_excel(xls_file, index=False)
        if (order_df["status"] == "Completed").any():
            pub_order_details ={
            "resource_id": resource_id,
            "Status": "Completed"
        }
            pub_order_details_json = json.dumps(pub_order_details)
            client.publish("order/operation/state/set", pub_order_details_json)
        else:
            print("Something went wrong when updating the order state to Completed.")   

def count_order_in_df(o_no, o_pos, pallet_id, order_df):
    count_order = order_df[
        (order_df["order_no"] == o_no) &
        (order_df["order_pos"] == o_pos) &
        (order_df["assignment"] == pallet_id)
    ]

    if count_order.empty:
        print("No order found with order_no:", o_no, "and order_pos:", o_pos)
        return 0
    else:
        return len(count_order)


