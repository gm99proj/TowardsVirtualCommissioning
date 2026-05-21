def connect_mqtt_broker(connect_mqtt, log, messagebox):
    try:
        connect_mqtt()
        log("MQTT Connected")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def sim_connect_mqtt_broker(connect, log, messagebox):
    try:
        connect()
        log("Closed Loop MQTT Connected")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def order_info_pub(connect, log, messagebox):
    try:
        connect()
        log("Order Info Published")
    except Exception as e:
        messagebox.showerror("Error", str(e))