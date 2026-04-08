import win32com.client

try:
    ps = win32com.client.Dispatch("Tecnomatix.PlantSimulation.RemoteControl.25.4")
    print("SUCCESS")
except Exception as e:
    print("ERROR:", e)