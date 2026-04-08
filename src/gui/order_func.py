from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk


def new_order(parent, order_dropdown, output_label, order_list, order_counter_ref):
    def save_order():
        part = part_var.get()
        qty_text = quantity_entry.get()

        if not part:
            messagebox.showerror("Error", "Select a part")
            return

        if not qty_text.isdigit():
            messagebox.showerror("Error", "Enter valid quantity")
            return

        quantity = int(qty_text)
        order_no = order_counter_ref[0]

        order = {
            "order_no": order_no,
            "part": part,
            "quantity": quantity
        }

        order_list.append(order)

        # update dropdown in main window
        order_dropdown['values'] = [o["order_no"] for o in order_list]

        order_counter_ref[0] += 1

        output_label.config(text=f"Created {order_no}")
        popup.destroy()

    # ---------- POPUP ----------
    popup = tk.Toplevel(parent)
    popup.title("New Order")
    popup.geometry("250x200")

    # Part selection
    tk.Label(popup, text="Part ID").pack()
    part_var = tk.StringVar()
    part_dropdown_popup = ttk.Combobox(popup, textvariable=part_var)
    part_dropdown_popup['values'] = ["1214", "1213", "1211", "1210"]
    part_dropdown_popup.pack(pady=5)

    # Quantity input
    tk.Label(popup, text="Quantity").pack()
    quantity_entry = tk.Entry(popup)
    quantity_entry.pack(pady=5)

    tk.Button(popup, text="Save Order", command=save_order).pack(pady=10)

def view_order(parent, order_list):
    popup = tk.Toplevel(parent)
    popup.title("View Orders")
    popup.geometry("300x300")

    if not order_list:
        tk.Label(popup, text="No orders available").pack()
        return

    listbox = tk.Listbox(popup, width=40)
    listbox.pack(pady=10)

    # Fill list
    for o in order_list:
        listbox.insert(tk.END, f"{o['order_no']} | Part:{o['part']} | Qty:{o['quantity']}")

    def show_details():
        selection = listbox.curselection()
        if not selection:
            return

        index = selection[0]
        order = order_list[index]

        details_label.config(
            text=f"Order No: {order['order_no']}\nPart: {order['part']}\nQuantity: {order['quantity']}"
        )

    tk.Button(popup, text="Show Details", command=show_details).pack()

    details_label = tk.Label(popup, text="", justify="left")
    details_label.pack(pady=10)

def publish_order(order_select_var, order_list, output_label, publish_message, messagebox, create_order):
    try:
        selected = order_select_var.get()
        selected = int(selected)

        if not selected:
            messagebox.showerror("Error", "Select an order")
            return

        # Extract order number

        order = next((o for o in order_list if o["order_no"] == selected), None)

        if not order:
            messagebox.showerror("Error", "Order not found")
            return

        json_data = create_order(
            order["order_no"],
            order["part"],
            order["quantity"]
        )

        publish_message(json_data)

        output_label.config(text=f"Published {order['order_no']}")

    except Exception as e:
        messagebox.showerror("Error", str(e))