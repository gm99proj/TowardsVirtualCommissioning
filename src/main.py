import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
#import pm05a7be59_501b_4906_82a4_1649b6fcae8d as MES_connect
from plantsim.plantsim import Plantsim as ps
from modules.connectMQTT import connect_mqtt, publish_message
from modules.createOrder import create_order

#GUI Functions
from gui.sim_func import sim_doc, sim_quit, sim_close, init_plantsim, set_event_controller, sim_start_stop, sim_reset
from gui.mqtt_connect import connect_mqtt_broker
from gui.order_func import new_order, view_order, publish_order

global plantsim
global default

order_counter = [1]  # Using a list to allow modification inside functions
order_list = []

plantsim = ps(license_type='Educational')
default = '.Models.Model'


# Create main window
Layout = tk.Tk()
Layout.title("Plant Simulation Interface")
Layout.geometry("350x650")

#Functions setup from modules

# Simulation functions
init_plantsim_func = lambda: init_plantsim(Layout, filedialog, output_label, plantsim, messagebox)
set_event_controller_func = lambda: set_event_controller(plantsim, default, output_label, messagebox)
sim_start_stop_func = lambda: sim_start_stop(plantsim, output_label, messagebox)
sim_reset_func = lambda: sim_reset(plantsim, output_label, messagebox)
sim_doc_func = lambda: sim_doc(plantsim, output_label)
sim_quit_func = lambda: sim_quit(plantsim, Layout, messagebox)
sim_close_func = lambda: sim_close(plantsim, output_label, messagebox)            

# MQTT function
connect_mqtt_func = lambda: connect_mqtt_broker(connect_mqtt, output_label, messagebox)    

# Order functions
new_order_func = lambda: new_order(Layout, order_dropdown, output_label, order_list, order_counter)
view_order_func = lambda: view_order(Layout, order_list)
publish_order_func = lambda: publish_order(order_select_var, order_list, output_label, publish_message, messagebox, create_order)

#Buttons

# Simulation Buttons
tk.Button(Layout, text="Load Model", command=init_plantsim_func).pack(pady=5)
tk.Button(Layout, text="Set Event Controller", command=set_event_controller_func).pack(pady=5)
tk.Button(Layout, text="Start/Stop Simulation", command=sim_start_stop_func).pack(pady=5)
tk.Button(Layout, text="Reset Simulation", command=sim_reset_func).pack(pady=5)
tk.Button(Layout, text="Documentation", command=sim_doc_func).pack(pady=5)
tk.Button(Layout, text="Close", command=sim_close_func).pack(pady=5)
tk.Button(Layout, text="Quit", command=sim_quit_func).pack(pady=5)

# MQTT Button
tk.Button(Layout, text="Connect MQTT", command=connect_mqtt_func).pack(pady=5)

# Order Buttons
tk.Button(Layout, text="New Order", command=new_order_func).pack(pady=5)
tk.Button(Layout, text="View Order", command=view_order_func).pack(pady=5)
tk.Button(Layout, text="Publish Order", command=publish_order_func).pack(pady=5)

# Order dropdown
order_select_var = tk.StringVar()

order_dropdown = ttk.Combobox(Layout, textvariable=order_select_var)
order_dropdown.pack(pady=5)


# Output label
output_label = tk.Label(Layout, text="", wraplength=280, justify="left")
output_label.pack(pady=10)


# Run the app
Layout.mainloop()