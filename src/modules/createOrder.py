import json

def get_workplan(partID):
    workplan_mapping = {
        "1214-Product with PCB & 2 Fuses": "1",
        "1213-Product with PCB & 1 Fuse": "2",
        "1211-Product with only PCB": "4",
        "1210-Product without PCB & Fuse": "7",
        "1111-Sample Product": "2"
    }
    return workplan_mapping.get(partID, "0")

def conceptualize_order(orderID,partID,quantity):
    orderQueue = []

    for pos in range(1, quantity + 1):
        order = {
            "order_no": orderID,
            "position": pos,
            "resource": "1",
            "workplan": get_workplan(partID),
            "step": "10",
            "part": f"{partID}"
        }
        orderQueue.append(order)
    return json.dumps(orderQueue, indent=2)

def create_order(orderID,partID,quantity):
    orderQueue = []

    for pos in range(1, quantity + 1):
        order = {
            "order_no": orderID,
            "position": pos,
            "resource": "65",
            "workplan": get_workplan(partID),
            "step": "10",
            "part": f"{partID}"
        }
        orderQueue.append(order)
    return json.dumps(orderQueue, indent=2)
