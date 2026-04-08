To establish a connection between external Python and the Plant Simulation, there are some required versions to be fulfilled

***Python Version = 3.8 or less***
Current Project setup is on Py 3.8 

Note: If you have a different version of Python, it's better to create a virtual env(venv) for the Py 3.8 version and ensure the Py version is set in your desktop, and setup Virtual env through the command: (py -3.8 -m venv "Give any folder title") in your desired folder

***pywin32==225***

Very important library because this is one prerequisite for the Plant simulation library to install it in the venv 
    1- Go to the venv folder
    2- Open CMD and activate the env by (Scripts\activate)
    3- pip install pywin32==225

**Note**: You might encounter issues importing the plantsim lib when running any scripts. The error looks like this (ImportError: DLL load failed: The specified module could not be found). To resolve this, copy the dll found in ("Your venv"\Lib\site-packages\pywin32_system32") and paste it in ("Your venv"\Lib\site-packages\win32)

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

Note: These libraries are important to run the script in place under /src.

To get started with the actually working POC of MQTT with Plant simulation
