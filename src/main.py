import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
#import pm05a7be59_501b_4906_82a4_1649b6fcae8d as MES_connect
from plantsim.plantsim import Plantsim as ps
from modules.connectMQTT import connect_mqtt, publish_message
from modules.createOrder import create_order, conceptualize_order
from modules.MES_display import update_resource_table, resource_ids, conceptual_resource_ids, reset_mes
from modules.ActualMES_com import order_info_publish
from modules.sim_ConnectMQTT import client_setup

#GUI Functions
from gui.sim_func import sim_doc, sim_quit, sim_close, init_plantsim, set_event_controller, sim_start_stop, sim_reset
from gui.mqtt_connect import connect_mqtt_broker, sim_connect_mqtt_broker, order_info_pub
from gui.order_func import new_order, view_order, publish_order


order_list = []
update_job = None

plantsim = ps(license_type='Educational')
default = '.Models.Model'


# Create main window
Layout = tk.Tk()
Layout.title("Plant Simulation Interface")
Layout.rowconfigure(0, weight=1)
Layout.columnconfigure(0, weight=1)

#Functions setup from modules

# Simulation functions
init_plantsim_func = lambda: init_plantsim(Layout, filedialog, log, plantsim, messagebox)
set_event_controller_func = lambda: set_event_controller(plantsim, default, log, messagebox)
sim_start_stop_func = lambda: sim_start_stop(plantsim, log, messagebox)
sim_reset_func = lambda: sim_reset(plantsim, log, messagebox)
sim_doc_func = lambda: sim_doc(plantsim, log, messagebox)
sim_quit_func = lambda: sim_quit(plantsim, Layout, messagebox)
sim_close_func = lambda: sim_close(plantsim, log, messagebox)            

# MQTT functioncl
connect_mqtt_func = lambda: connect_mqtt_broker(connect_mqtt, log, messagebox)

#MES functions
order_info_func = lambda: order_info_pub(order_info_publish, log, messagebox)
sim_connect_mqtt = lambda: sim_connect_mqtt_broker(client_setup, log, messagebox)


# Order functions
new_order_func = lambda: new_order(Layout, order_dropdown, log, order_list)
view_order_func = lambda: view_order(Layout, order_list)
publish_order_func = lambda: publish_order(order_select_var, order_list, log, publish_message, messagebox, conceptualize_order if conceptual_var.get() else create_order)

def switch_mes_table():
    global update_job

    # STOP OLD LOOP
    if update_job is not None:
        tree.after_cancel(update_job)
        update_job = None

    # CLEAR TABLE
    for item in tree.get_children():
        tree.delete(item)

    # -----------------------------------------
    # CONCEPTUAL MODE
    # -----------------------------------------

    if conceptual_var.get():

        # INSERT CONCEPTUAL RESOURCES
        for res_id, name in conceptual_resource_ids.items():

            tree.insert("", "end", iid=str(res_id), values=( f"{res_id} - {name}", "Free", "-", "-"), tags=("Free",))

        update_job = update_resource_table(
            tree,
            "src/database/order_state.xlsx",
            conceptual=True
        )

        print("Switched to Conceptual MES")

    # -----------------------------------------
    # REAL MODE
    # -----------------------------------------

    else:

        # INSERT REAL RESOURCES
        for res_id, name in resource_ids.items():

            tree.insert("", "end", iid=str(res_id), values=(f"{res_id} - {name}", "Free", "-", "-"), tags=("Free",))

        update_job = update_resource_table(
            tree,
            "src/database/order_state.xlsx"
        )

        print("Switched to Real MES")

# ---------- MAIN CONTAINER ----------
main_frame = tk.Frame(Layout)
main_frame.grid(row=0, column=0, sticky="nsew")

main_frame.columnconfigure(0, weight=1)   # left (tabs)
main_frame.columnconfigure(1, weight=2)   # right (output)
main_frame.rowconfigure(0, weight=1)

# ---------- LEFT SIDE (TABS) ----------
left_panel = tk.Frame(main_frame, padx=10, pady=10)
left_panel.grid(row=0, column=0, sticky="nsew")

left_panel.rowconfigure(0, weight=1)
left_panel.columnconfigure(0, weight=1)

notebook = ttk.Notebook(left_panel)
notebook.grid(row=0, column=0, sticky="nsew")   

# ================= SIMULATION TAB =================
sim_tab = tk.Frame(notebook)
notebook.add(sim_tab, text="Simulation")

sim_tab.rowconfigure(0, weight=1)
sim_tab.columnconfigure(0, weight=1)

tk.Button(sim_tab, text="Load Model", width=15, command=init_plantsim_func).pack(pady=5)
tk.Button(sim_tab, text="Set Controller", width=15, command=set_event_controller_func).pack(pady=5)
tk.Button(sim_tab, text="Start/Stop", width=15, command=sim_start_stop_func).pack(pady=5)
tk.Button(sim_tab, text="Reset", width=15, command=sim_reset_func).pack(pady=5)
tk.Button(sim_tab, text="Documentation", width=15, command=sim_doc_func).pack(pady=5)
tk.Button(sim_tab, text="Close", width=15, command=sim_close_func).pack(pady=5)
tk.Button(sim_tab, text="Quit", width=15, command=sim_quit_func).pack(pady=5)

# ================= ORDERS TAB =================
order_tab = tk.Frame(notebook)
notebook.add(order_tab, text="Orders")

order_tab.rowconfigure(0, weight=1)
order_tab.columnconfigure(0, weight=1)

tk.Button(order_tab, text="New Order", width=15, command=new_order_func).pack(pady=5)
tk.Button(order_tab, text="View Orders", width=15, command=view_order_func).pack(pady=5)
tk.Button(order_tab, text="Publish Order", width=15, command=publish_order_func).pack(pady=10)

order_select_var = tk.StringVar()
conceptual_var = tk.BooleanVar(value=False)
order_dropdown = ttk.Combobox(order_tab, textvariable=order_select_var)
order_dropdown.pack(fill="x", pady=5)
tk.Checkbutton(
    order_tab,
    text="Conceptual Order",
    variable=conceptual_var,
    command=switch_mes_table
).pack(pady=5)

# ================= MQTT TAB =================
mqtt_tab = tk.Frame(notebook)
notebook.add(mqtt_tab, text="MQTT")

mqtt_tab.rowconfigure(0, weight=1)
mqtt_tab.columnconfigure(0, weight=1)

tk.Button(mqtt_tab, text="Connect MQTT", width=25, command=connect_mqtt_func).pack(pady=10)
tk.Button(mqtt_tab, text="Order Info from MES", width=25, command=order_info_func).pack(pady=10) 
tk.Button(mqtt_tab, text="Closed Loop Connection", width=25, command=sim_connect_mqtt).pack(pady=10)


#------------------- MES TAB -----------------
mes_tab = tk.Frame(notebook)
notebook.add(mes_tab, text="MES Simulator")

mes_tab.rowconfigure(0, weight=1)
mes_tab.columnconfigure(0, weight=1)

columns = ("Resource", "Status", "Operation", "Pallet")

tree = ttk.Treeview(mes_tab, columns=columns, show="headings")
tree.grid(row=0, column=0, sticky="nsew")

tree.heading("Resource", text="Resource")
tree.heading("Status", text="Status")
tree.heading("Operation", text="Operation")
tree.heading("Pallet", text="Pallet")

for col in columns:
    tree.column(col, stretch=True, width=120)

tree.tag_configure("Free", background="lightgreen")
tree.tag_configure("Busy", background="orange")

tree_scroll = tk.Scrollbar(mes_tab, orient="vertical", command=tree.yview)
tree_scroll.grid(row=0, column=1, sticky="ns")
tree.configure(yscrollcommand=tree_scroll.set)

tk.Button(
    mes_tab,
    text="Reset MES",
    command=lambda: reset_mes(tree, "src/database/order_state.xlsx")
).grid(row=1, column=0, pady=5)

switch_mes_table()

# ---------- RIGHT SIDE (OUTPUT PANEL) ----------
right_panel = tk.Frame(main_frame, padx=20, pady=10)
right_panel.grid(row=0, column=1, sticky="nsew")

right_panel.rowconfigure(0, weight=1)
right_panel.columnconfigure(0, weight=1)

output_frame = tk.LabelFrame(right_panel, text="Output / Status", padx=10, pady=10)
output_frame.grid(row=0, column=0, sticky="nsew")

output_frame.rowconfigure(0, weight=1)
output_frame.columnconfigure(0, weight=1)

# Text widget
output_text = tk.Text(output_frame, wrap="word")
output_text.grid(row=0, column=0, sticky="nsew")

# Scrollbar
scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

output_text.config(yscrollcommand=scrollbar.set)

# ---------- LOG FUNCTION ----------
def log(message):
    global output_text
    output_text.insert(tk.END, message + "\n")
    output_text.see(tk.END)


def clear_log():
    output_text.delete(1.0, tk.END)





# Run the app
Layout.mainloop()