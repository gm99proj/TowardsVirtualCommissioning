from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk


def new_order(parent, order_dropdown, log, order_list):
    def save_order():
        part = part_var.get()
        qty_text = quantity_entry.get()
        order_no_text = order_no_entry.get()

        if not order_no_text.isdigit():
            messagebox.showerror("Error", "Enter valid order number")
            return

        order_no = int(order_no_text)

        # check duplicate order number
        if any(o["order_no"] == order_no for o in order_list):
            messagebox.showerror("Error", "Order number already exists")
            return

        if not part:
            messagebox.showerror("Error", "Select a part")
            return

        if not qty_text.isdigit():
            messagebox.showerror("Error", "Enter valid quantity")
            return

        quantity = int(qty_text)

        order = {
            "order_no": order_no,
            "part": part,
            "quantity": quantity
        }

        order_list.append(order)

        # update dropdown
        order_dropdown['values'] = [o["order_no"] for o in order_list]

        log(f"Created order {order_no}")
        popup.destroy()

    # ---------- POPUP ----------
    popup = tk.Toplevel(parent)
    popup.title("New Order")
    popup.geometry("250x250")

    # Order number input (NEW)
    tk.Label(popup, text="Order Number").pack()
    order_no_entry = tk.Entry(popup)
    order_no_entry.pack(pady=5)

    # Part selection
    tk.Label(popup, text="Part ID").pack()
    part_var = tk.StringVar()
    part_dropdown_popup = ttk.Combobox(popup, textvariable=part_var)
    part_dropdown_popup['values'] = ["1214-Product with PCB & 2 Fuses", "1213-Product with PCB & 1 Fuse", "1211-Product with only PCB", "1210-Product without PCB & Fuse", "1111-Sample Product"]
    part_dropdown_popup.pack(pady=5)

    # Quantity input
    tk.Label(popup, text="Quantity").pack()
    quantity_entry = tk.Entry(popup)
    quantity_entry.pack(pady=5)

    tk.Button(popup, text="Save Order", command=save_order).pack(pady=10)


def view_order(parent, order_list):
    popup = tk.Toplevel(parent)
    popup.title("Orders Table")
    popup.geometry("600x350")

    if not order_list:
        tk.Label(popup, text="No orders available").pack(pady=20)
        return

    # ---------- TABLE ----------
    columns = ("order_no", "part", "quantity")

    tree = ttk.Treeview(popup, columns=columns, show="headings")

    # Headings
    tree.heading("order_no", text="Order No")
    tree.heading("part", text="Part")
    tree.heading("quantity", text="Quantity")

    # Column formatting
    tree.column("order_no", width=100, anchor="center")
    tree.column("part", width=350)
    tree.column("quantity", width=100, anchor="center")

    # Insert data
    for o in order_list:
        tree.insert("", tk.END, values=(
            o["order_no"],
            o["part"],
            o["quantity"]
        ))

    tree.pack(fill="both", expand=True)

    def on_double_click(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            messagebox.showinfo("Details", f"{values}")

    tree.bind("<Double-1>", on_double_click)

    # Scrollbar
    scrollbar = tk.Scrollbar(popup, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")


def publish_order(order_select_var, order_list, log, publish_message, messagebox, create_order):
    try:
        selected = order_select_var.get()
        selected = int(selected)

        if not selected:
            messagebox.showerror("Error", "Select an order to publish")
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

        log(f"Published order {order['order_no']}")

    except Exception as e:
        messagebox.showerror("Error", str(e))