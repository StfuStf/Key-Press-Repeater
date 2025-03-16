# Key Press Repeater

A tool to automate key presses at specified intervals.

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/StfuStf/Key-Press-Repeater.git
   cd Key-Press-Repeater
Install the dependencies:

````bash
   pip install -r requirements.txt
````

2.Install the package:

````bash
python setup.py install
````


Steps to Add a Custom Icon on Linux:
1. Prepare the Icon File:
Use a .png file for the icon (e.g., app_icon.png).

Place the icon file in the same directory as your script or in a dedicated icons folder (e.g., /usr/share/icons/ or ~/.local/share/icons/).

2. Create a Desktop Entry:
Create a .desktop file to define your application and specify the icon.

Example .desktop file (xD.desktop):


````[Desktop Entry]
Name=Key Press Repeater
Exec=/path/to/dist/xD
Icon=/path/to/app_icon.png
Type=Application
Categories=Utility;Application;
Terminal=false
````
Replace /path/to/dist/xD with the full path to your executable.
Replace /path/to/app_icon.png with the full path to your icon file.

3. Save the Desktop Entry:
Save the .desktop file in ~/.local/share/applications/ (for the current user) or /usr/share/applications/ (for all users).

Example:

````bash
nano ~/.local/share/applications/xD.desktop
````
4. Make the Desktop Entry Executable:
Run the following command to make the .desktop file executable:

````bash
chmod +x ~/.local/share/applications/xD.desktop
````
Create the Executable:
Navigate to the directory where your script (xD.py) is located and run the following command:

bash
Copy
pyinstaller --onefile --windowed xD.py
--onefile: Packages everything into a single executable file.

--windowed: Prevents a terminal window from appearing (useful for GUI applications).

5. Locate the Executable:
After running the above command, PyInstaller will create a dist folder in the same directory as your script. Inside the dist folder, you'll find the standalone executable file (xD).

6. Run the Executable:
You can run the executable directly from the terminal:

````bash

./dist/xD
````
5. Distribute the Application:
You can distribute the xD executable to others. They won't need Python or any dependencies installed to run it.

Example: Packaging the Script
Assuming your script is named xD.py, here's how you can package it:

Open a terminal in the directory where xD.py is located.

Run the following command:

````bash
pyinstaller --onefile --windowed xD.py
````
After the process completes, find the executable in the dist folder:

````bash

./dist/xD
````
