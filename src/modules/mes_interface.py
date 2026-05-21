"""
MES4 Interface Service Classes and Numbers

This module provides an overview of MES4 service classes (MClass) and service numbers (MNo),
as documented in the MES4 Interfaces manual (Version 1.07).

### Service Classes (MClass)
| MClass | Description                                      |
|--------|--------------------------------------------------|
| 10     | Order state management (e.g., start, reset, end) |
| 100    | Query orders and work plans                      |
| 101    | Modify orders and work plans                     |
| 110    | Query topology                                   |
| 150    | Query buffer and utilities state                 |
| 151    | Modify buffer and utilities state                |
| 200    | Query transport orders and AGV-related data      |
| 201    | Modify transport orders and AGV-related data     |

### Notable Services (MClass, MNo, Description)

#### MClass 10 (Order State Management)
| MNo | Service Name | Description                                      |
|-----|--------------|--------------------------------------------------|
| 10  | OpStart      | Starts an order                                  |
| 15  | OpReset      | Resets an already started order                  |
| 20  | OpEnd        | Finishes an already started order                |

#### MClass 100 (Query Orders and Work Plans)
| MNo | Service Name            | Description                                      |
|-----|-------------------------|--------------------------------------------------|
| 4   | GetFirstOpForRsc        | Returns the first task of an order for a resource|
| 6   | GetOpForONoOPos         | Returns task details for a specific order        |
| 33  | GetStepDescription      | Returns the description of a step                |
| 111 | getFreeString           | Returns the free string parameter of a step      |

#### MClass 101 (Modify Orders and Work Plans)
| MNo | Service Name        | Description                                      |
|-----|---------------------|--------------------------------------------------|
| 1   | SetPar              | Writes parameter values for a step               |
| 2   | SetNewOrder         | Creates a new order                              |
| 6   | SetCustomerOrder    | Creates a new customer order                      |

#### MClass 150 (Query Buffer and Utilities State)
| MNo | Service Name    | Description                                      |
|-----|-----------------|--------------------------------------------------|
| 5   | GetBufPos       | Returns buffer position information              |


"""

import configparser
import json
import logging
import socket
import struct
import sys
import time
from typing import Dict
from logging.handlers import RotatingFileHandler
import paho.mqtt.client as mqtt

# ---------------------------------------------------------------------------
# MES query constansts (from desc above) 
# ---------------------------------------------------------------------------

# MES4 Service Classes (MClass)
MCLASS_ORDER_STATE = 10
MCLASS_QUERY_ORDERS = 100
MCLASS_MODIFY_ORDERS = 101
MCLASS_QUERY_TOPOLOGY = 110
MCLASS_QUERY_BUFFER = 150
MCLASS_MODIFY_BUFFER = 151
MCLASS_QUERY_TRANSPORT = 200
MCLASS_MODIFY_TRANSPORT = 201

# MES4 Service Numbers (MNo) for MClass 10 (Order State)
MNO_OP_START = 10
MNO_OP_RESET = 15
MNO_OP_END = 20

# MES4 Service Numbers (MNo) for MClass 100 (Query Orders)
MNO_GET_FIRST_OP_FOR_RESOURCE = 4
MNO_GET_OP_FOR_ONO_OPOS = 6
MNO_GET_ORDER_INFO = 30
MNO_GET_STEP_DESCRIPTION = 33
MNO_GET_FREE_STRING = 111

# MES4 Service Numbers (MNo) for MClass 101 (Modify Orders)
MNO_SET_PARAMETER = 1
MNO_SET_NEW_ORDER = 2
MNO_SET_CUSTOMER_ORDER = 6

# MES4 Service Numbers (MNo) for MClass 150 (Query Buffer)
MNO_GET_BUF_POS = 5

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

config = configparser.ConfigParser()


if not config.read("src\\modules\\config.ini"):
    print("ERROR: config.ini not found. Please create it next to this script.")
    sys.exit(1)

MES4_IP           = config.get("mes4", "ip")
MES4_PORT_SERVICE = config.getint("mes4", "port_service")
MES4_PORT_CYC     = config.getint("mes4", "port_cyclic")

RESOURCE_ID       = config.getint("mes4", "resource_id")
# trick loads multiple resource ids as a list from an .ini file
RESOURCE_IDS       = json.loads(config.get("mes4", "resource_ids"))

MAX_POSITIONS     = config.getint("mes4", "max_positions")
ORDER_SCAN_RANGE  = config.getint("mes4", "order_scan_range")

MQTT_BROKER       = config.get("mqtt", "broker")
MQTT_PORT         = config.getint("mqtt", "port")
MQTT_TOPIC_BASE   = config.get("mqtt", "topic_base")
MQTT_TOPIC_SIM    = config.get("mqtt", "topic_sim")

POLL_INTERVAL     = config.getint("general", "poll_interval")
LOG_FILE          = config.get("general", "log_file")
LOG_LEVEL         = config.get("general", "log_level").upper()
CONST_PUBLISH     = config.get("general", "const_publish")

BUFFER_SIZE = 2048

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger("mes4")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Rotating file handler — max 5 MB per file, keep 3 backups
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ---------------------------------------------------------------------------
# Helpers for binary message construction (unused in string mode)
# ---------------------------------------------------------------------------

msg_service = bytearray(128)

def write_int16(offset, value):
    struct.pack_into("<H", msg_service, offset, value)

def write_int32(offset, value):
    struct.pack_into("<I", msg_service, offset, value)

def write_uint8(offset, value):
    struct.pack_into("<B", msg_service, offset, value)

def make_status_byte(bit0=False, bit1=False, bit2=False, bit3=False,
                     bit4=False, bit5=False, bit6=False, bit7=False):
    value = 0
    for i, bit in enumerate([bit0, bit1, bit2, bit3, bit4, bit5, bit6, bit7]):
        value |= int(bit) << i
    return value


# ---------------------------------------------------------------------------
# Cyclic update message
# ---------------------------------------------------------------------------

msg_cyclic = bytearray(4)
struct.pack_into("<H", msg_cyclic, 0, RESOURCE_ID)  # ResourceID (must match MES4)
struct.pack_into("<B", msg_cyclic, 2, 1)             # PLC Type (1 = little endian / CoDeSys)
status_byte = make_status_byte(bit7=True)            # Status: MES-mode active
struct.pack_into("<B", msg_cyclic, 3, status_byte)

message_update = bytes(msg_cyclic)


# ---------------------------------------------------------------------------
# Service call helpers
# ---------------------------------------------------------------------------

def send(sock: socket.socket, msg: str) -> Dict[str, str]:
    """Send a string-encoded service request and return the parsed response. Also sleeps a bit before looking for a response."""

    final_msg = msg.encode("ascii") + b"\r"

    logger.debug(f"Sending msg {final_msg}")

    sock.sendall(final_msg)
    time.sleep(0.1)
    raw = sock.recv(BUFFER_SIZE).decode("ascii", errors="replace")
    parts = raw.strip().rstrip("*\r\n").split(";")
    result = {}
    for part in parts[1:]:  # skip TcpIdent
        if "=" in part:
            key, _, value = part.partition("=")
            result[key.strip()] = value.strip()
    return result

def get_first_op_for_resource(resource_id):
    """MNo=4: Get the first pending task assigned to a resource. This only works with the very first resource for an order, will not work with subsequent ones. They will return as if there's no order on them.""" 

    return f"444;RequestId={resource_id};MClass={MCLASS_QUERY_ORDERS};MNo={MNO_GET_FIRST_OP_FOR_RESOURCE};#ResourceID={resource_id}"

def get_op_details(order_no, order_pos, request_id=0):
    """MNo=6: Get full task details for a specific order + position."""

    return f"444;RequestId={request_id};MClass={MCLASS_QUERY_ORDERS};MNo={MNO_GET_OP_FOR_ONO_OPOS};#ONo={order_no};#OPos={order_pos}"

def get_order_info(order_no, request_id=0):
    """MNo=30: Check if an order exists and get its customer number."""

    return f"444;RequestId={request_id};MClass={MCLASS_QUERY_ORDERS};MNo={MNO_GET_ORDER_INFO};#ONo={order_no}"

def get_step_description(order_no, order_pos, request_id=0):
    """MNo=33: Get the text description of the current step."""

    return f"444;RequestId={request_id};MClass={MCLASS_QUERY_ORDERS};MNo={MNO_GET_STEP_DESCRIPTION};#ONo={order_no};#OPos={order_pos}"
