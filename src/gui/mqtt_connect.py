def connect_mqtt_broker(connect_mqtt, output_label, messagebox):
    try:
        connect_mqtt()
        output_label.config(text="MQTT Connected")
    except Exception as e:
        messagebox.showerror("Error", str(e))