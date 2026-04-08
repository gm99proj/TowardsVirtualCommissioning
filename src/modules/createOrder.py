import json

def get_workplan(partID):
    workplan_mapping = {
        "1214": "1",
        "1213": "2",
        "1211": "4",
        "1210": "7"
    }
    return workplan_mapping.get(partID, "0")


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
