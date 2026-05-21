# Virtual commissioning (Plant Simulation with MQTT)

## Project Brief

Python COM interface 

MQTT

Plant simulation

Content to be added


## Setup
To establish a connection between external Python and the Plant Simulation, there are some required versions to be fulfilled

***Python Version = 3.8 or less***
Current Project setup is on Py 3.8 

**Note**: If you have a different version of Python, it's better to create a virtual env(venv) for the Py 3.8 version and ensure the Py version is set in your desktop, and setup Virtual env through the command: ***py -3.8 -m venv "Give any folder title"*** in your desired folder

>[!IMPORTANT]
> ***pywin32==225***: Very important library for the Plant simulation module to install in the venv
>    1. Go to the venv folder
>    2. Open CMD and activate the env by (Scripts\activate)
>    3. pip install pywin32==225

>[!NOTE]
> You might encounter issues importing the plantsim lib when running any scripts. The error looks like this (*ImportError: DLL load failed: The specified module could not be found*). To resolve this, copy the dll found in (***"Your venv"\Lib\site-packages\pywin32_system32"***) and paste it in (***"Your venv"\Lib\site-packages\win32***)

List of Virtual Env Libraries:

|Package       |  Version   |
| ------------ | ---------- |
|mqtt          |  0.0.1     |  
|numpy         |  1.24.4    |  
|paho-mqtt     |  1.6.1     |  
|pandas        |  2.0.3     |  
|pip           |  19.2.3    |  
|plantsim      |  0.0.3     |  
|python-dateutil| 2.9.0.post0| 
|pytz          |  2026.1.post1|
|pywin32       |  225       |  
|setuptools    |  41.2.0    |  
|six           |  1.17.0    |  
|texttable     |  1.7.0     |  
|tzdata        |  2025.3    |

>[!NOTE]
>These libraries are important to run the script in place under /src.


## WORKING POC

**Get started with the actually working POC of MQTT with the Plant Simulation (PS)**

1. To start goto *\src* folder and run ***main.py***.

2. Wait until the Python GUI is displayed, and the PS is opened (see the image).

    <p align= "center"><img width="640" height="480" alt="image" label= "Initial step" src="https://github.com/user-attachments/assets/14b932a7-462a-4272-af71-cdeb1d78abb3" /></p>

3. The GUI contains a lot of buttons to simplify the button functions, which are explained here:
    - *Load Model* = This helps the user select and load the desired PS file/model (***___.spp***) into the PS application.
    - *Set Event Controller* = This is a **Mandatory** function or to be clicked before starting the simulation.
    - *Start/Stop Simulation* = This interacts with the start and stop of the simulation.
    - *Reset Simulation* = This function resets the simulation.
    - *Documentation* = This function prints the methods that are utilized for the Python COM interface to interact with PS.
    - *Close* = This function closes the current model present in the PS application.
    - *Quit* = This function closes the entire PS application and GUI.
    - *Connect MQTT* = This helps in setting up an MQTT client server and establishing a MQTT broker for communication.
    - *New Order* = This function emulates a MES order creation system.
    - *View Order* = This function emulates a MES order viewing system.
    - *Publish Order* = This function emulates a MES order-generating system that connects the MQTT broker to publish the data/information
    - *Simple Dropdown* = To select the created order for publishing.
   
4. Now click on *Load model* and select the ***SL_V07_MQTT.spp*** available in the folder.

    <p align = "center"><img src="/media/load_model.gif" width="640" height="480"/></p>

5. Click on *Connect MQTT* to establish an MQTT broker connection.

    <p align = "center"><img src="/media/connect_mqtt.gif" width="640" height="480"/></p>

6. In the PS application, there exists a Method (*orderAssignment*) file. Right-click on it and select the *Run* option from the menu. In the PS, observe that the MQTT interface has green and orange rectangular blocks at the top, indicating that the MQTT broker connection is linked.

    <p align = "center"><img src="/media/ps_connect_mqtt.gif" width="640" height="480"/></p>

7.  Now click on *Set Event Controller*.

   <p align = "center"><img src="/media/event_controller.gif" width="640" height="480"/></p>

8.  Create a simple order using *New Order*.

   <p align = "center"><img src="/media/new_order.gif" width="640" height="480"/></p>

9.  Once created, select the order from the dropdown and click on *Publish Order*. Observe that in the PS application console shows *Order transfer to simulation: Complete*.

   <p align = "center"><img src="/media/publish_order.gif" width="640" height="480"/></p>

10. The pushed order is placed in the Datatable(PS Excel form): *orderQueue*.

    <p align= "center"><img width="640" height="480" alt="order_queue" src="https://github.com/user-attachments/assets/ee33d4f4-17db-4856-ad1c-cb5e1a57fade" /></p>

11. The input for the simulation is taken from *orderQueue*.
12. Click on *Start/Stop Simulation* for the simulation start.

    <p align = "center"><img src="/media/simulation.gif" width="640" height="480"/></p>


13. Check the Datatable: *prodArchieve* to find the orders assigned to the pallet.

    <p align= "center"><img width="640" height="480" alt="prod_archieve" src="https://github.com/user-attachments/assets/0a860405-2841-439e-8638-0107ecff087a" /></p>


*Feel free to play around with the creation and publishing of orders and observe the simulation*

>[!NOTE]
>If the simulation resets, repeat from step 6 (exclude step 7 as the model is already assigned to a *Event Controller*)
    

