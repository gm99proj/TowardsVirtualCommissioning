# Towards Plant-Level Virtual Acceptance Testing (VAT)

This repository contains the implementation and research work focused on integrating a simulation model with a Manufacturing Execution System (MES4) to support plant-level Virtual Acceptance Testing (VAT).

The project is based on the **AAU 5G Smart Production Lab FESTO Assembly Line** and uses **Siemens Tecnomatix Plant Simulation** to create a virtual representation of the physical manufacturing system.

The implementation is divided into multiple phases, starting from the development of a standalone simulation model and extending toward MES communication and bidirectional synchronization.

---

# Project Overview

The project focuses on:

- Development of a simulation model of the FESTO assembly line
- Simulation workflow validation
- SimTalk-based control logic
- Integration between Plant Simulation and MES4
- MQTT-based communication architecture
- Virtual validation of manufacturing workflows

The overall goal is to create a foundation for:

- Digital Twin development
- MES-level validation
- Virtual commissioning
- Plant-level Virtual Acceptance Testing (VAT)

---

# Repository Structure

```bash
├── README.md
├── docs/
│   ├── simulation_setup_README.md
│   ├── phase1_README.md
│   └── phase2_README.md
├── GitHub_media/
├── PlantSim_Files/
├── python38_PSenv/
├── src/
└── mes4.log
└── requirements.txt

```

---

# Documentation

## Simulation Setup

This section explains how the simulation model of the FESTO assembly line was created using Siemens Tecnomatix Plant Simulation.

- CAD model preparation
- Simulation object creation
- Material flow setup
- SimTalk logic implementation
- Workflow validation

[Simulation Setup](docs/simulation_setup_README.md)

---

## Phase 1 — One-Way Communication

This phase demonstrates the implementation of one-way communication between the MES4 system and the simulation model.

Main focus areas:

- TCP/IP communication
- MQTT publishing
- Data transfer from MES to simulation
- Message interpretation inside Plant Simulation

[Phase 1 Documentation](docs/phase1_README.md)

---

## Phase 2 — Two-Way Communication

This phase demonstrates bidirectional communication between the simulation environment and the MES4 system.

Main focus areas:

- Two-way MQTT communication
- Request-response workflow
- Simulation feedback to MES
- Synchronization between virtual and physical systems

[Phase 2 Documentation](docs/phase2_README.md)

---

# Python Environment Setup

To establish communication between external Python applications and Siemens Plant Simulation, the following setup is required.

## Required Python Version

```text
Python 3.8 or lower
```

Current project environment is based on **Python 3.8**.

---

## Create Virtual Environment

```bash
py -3.8 -m venv plantsim_env
```

Activate the environment:

```bash
plantsim_env\\Scripts\\activate
```

---

# Required Python Libraries

The following libraries are used in the virtual environment for communication between Python, MES4, MQTT, and Plant Simulation.

| Package | Version |
|---|---|
| et-xmlfile | 2.0.0 |
| mqtt | 0.0.1 |
| numpy | 1.24.4 |
| openpyxl | 3.1.5 |
| paho-mqtt | 1.6.1 |
| pandas | 2.0.3 |
| plantsim | 0.0.3 |
| pywin32 | 225 |
| python-dateutil | 2.9.0.post0 |
| pytz | 2025.1 |
| setuptools | 41.2.0 |
| six | 1.17.0 |
| texttable | 1.7.0 |
| tzdata | 2025.2 |

---

## Install All Dependencies

```bash
pip install -r requirements.txt
```

>[!NOTE]
> The `requirements.txt` file contains all required libraries for running the scripts inside the `/src` folder.

---

## Important Dependency

>[!IMPORTANT]
> `pywin32==225` is required for communication between Python and Siemens Plant Simulation.

## Fix DLL Import Issue

If you encounter:

```text
ImportError: DLL load failed
```

Copy the DLL from:

```text
<venv>\\Lib\\site-packages\\pywin32_system32
```

to:

```text
<venv>\\Lib\\site-packages\\win32
```

---

# MES4 Connection Overview

MES4 communication is established using a **TCP/IP Request-Response** architecture.

The implementation uses:

- Service calls
- String encoding
- TCP/IP socket communication

---

# MES4 Services Used

| Service | Purpose |
|---|---|
| GetFirstOpForRsc | Retrieve first operation |
| GetOpForONoOPos | Retrieve order details |
| OpStart | Start operation |
| OpEnd | End operation |

---

# Example MES4 Request String Format

```text
444;RequestID=1;MClass=100;MNo=4;#ResourceID=1
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Siemens Plant Simulation | Simulation Environment |
| SimTalk | Simulation Logic |
| Python | External Interface |
| MQTT | Communication Protocol |
| TCP/IP | MES Communication |
| MES4 | Manufacturing Execution System |

---

# Future Development

Future improvements include:

- Real-time PLC integration
- OPC UA support
- Product customization
- Advanced Digital Twin synchronization
- Full Virtual Acceptance Testing implementation