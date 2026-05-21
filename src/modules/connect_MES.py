import socket
import time
import modules.mes_interface as mes

InitialresourceID = 65

def parse_message(msg):
    
    parts = msg.strip().rstrip("*\r\n").split(";")
    result = {}
    for part in parts[1:]:  # skip TcpIdent
        if "=" in part:
            key, _, value = part.partition("=")
            result[key.strip()] = value.strip()
    return result
    
def do_request(msg_bytes):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((mes.MES4_IP, mes.MES4_PORT_SERVICE))
    sock.sendall(msg_bytes.encode("ascii") + b"\r")
    return sock.recv(mes.BUFFER_SIZE).decode("ascii", errors="replace")
  finally:
    sock.close()

def discover_orders(sock, start_order):

    found = {}

    order_no = start_order

    info = mes.send(sock, mes.get_order_info(order_no))


    if info.get("ErrorState") != "0" or not info.get("ONo"):
        return found
    
    found[order_no] = []

    # scanning for n number of order positions
    start_time = time.perf_counter()
    counter = 0
    for pos in range(1, mes.MAX_POSITIONS + 1):
        details = mes.send(sock, mes.get_op_details(order_no, pos))
        print(f"Queried order {order_no} position {pos}: {details}")

        if details.get("ErrorState") != "0" or not details.get("ONo"):
            break

        found[order_no].append({
            "order_no": order_no,
            "position": pos,
            # since now we're publishing under the topic resource_id, this is redundant
            "resource": details.get("ResourceID", "?"),
            "workplan": details.get("WPNo", "?"),
            "step":     details.get("StepNo", "?"),
            "part":     details.get("PNo", "?"),
        })
        counter += 1

    return found

def initial_OrderMESRequest():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5.0)
            sock.connect((mes.MES4_IP, mes.MES4_PORT_SERVICE))

            # Check for a pending task on our resource
            # data = mes.send(sock, mes.get_first_op_for_resource(mes.RESOURCE_ID))
            data = mes.send(sock, mes.get_first_op_for_resource(InitialresourceID))
            # data = mes.send(sock, mes.get_order_info(1749, resource_id))

            order_no  = data.get("ONo")
            order_pos = data.get("OPos")

            if order_no and order_no != "0":
                found_order_number = int(order_no)
            else:
                print(f"No active task for resource {InitialresourceID}")
                # since we can't do anything anymore, we return empty
                return

            orders = discover_orders(sock, found_order_number)

            return orders
    
    except ConnectionRefusedError:
        print(f"Could not connect to MES4 at {mes.MES4_IP}:{mes.MES4_PORT_SERVICE} "
              "Please ensure the MES4 service is running and accessible.")
    except Exception as e:
        print(f"Unexpected error: {e}")