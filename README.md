1. main.py
The entry point to run the application...

2. pom_generator/controller.py
Handles the interaction between the UI (view.py) and the Playwright functions (model.py).

3. pom_generator/view.py
Defines the Tkinter UI components and manages UI updates.

4. pom_generator/model.py
Handles interaction with Playwright for retrieving selectors and generating the POM.

5. pom_generator/utils.py
Helper functions for generating selectors based on priorities and other utilities.


-----------------------------------------------------------------------
**Steps to Create an Executable File**
Step 1: Install PyInstaller
If you haven't already, install PyInstaller using pip:

bash
Copy code
pip install pyinstaller
Step 2: Organize the Project Files
Ensure your project has a clear directory structure. For example:

plaintext
Copy code
project-root/
├── main.py                   # Main entry point for the application
├── pom_generator/
│   ├── __init__.py
│   ├── controller.py
│   ├── view.py
│   ├── model.py
│   ├── utils.py
├── resources/
│   └── icon.png              # Optional: icon for the executable
└── requirements.txt          # List of dependencies (optional)
Make sure that main.py is the entry point of your application (the file with the if __name__ == "__main__": line).

Step 3: Run PyInstaller to Build the Executable
Navigate to your project’s root directory in the terminal and use PyInstaller to build the executable:

bash
Copy code
pyinstaller --onefile --windowed main.py
--onefile: This flag packages the application into a single executable file.
--windowed: This flag suppresses the command prompt window (for GUI applications on Windows).
If you have a custom icon (e.g., icon.png in the resources directory), you can add it with the --icon option:

bash
Copy code
pyinstaller --onefile --windowed --icon=resources/icon.ico main.py
Note: Convert your icon to .ico format if it isn’t already, as PyInstaller requires .ico for icons.

Step 4: Locate the Executable File
After PyInstaller finishes, you’ll find the executable in the dist folder inside your project directory:

plaintext
Copy code
project-root/
└── dist/
    └── main.exe          # The generated executable file (on Windows)
Step 5: Testing and Distribution
Testing: Run the executable (main.exe on Windows) to ensure it works as expected.
Distribution: Share the dist/main.exe file with users. For a standalone setup, you can compress the dist folder into a .zip file for easy distribution.
Handling Dependencies
If your project has additional dependencies listed in requirements.txt, ensure they are installed in your environment before running PyInstaller.

Additional Notes
Including External Files: If you need to include additional files (e.g., resources/icon.png), you can use the --add-data option:

bash
Copy code
pyinstaller --onefile --windowed --add-data "resources/icon.png;resources" main.py
The format is source_path;destination_path. PyInstaller will package icon.png and unpack it into a resources folder next to the executable.

Troubleshooting: If you encounter any issues, PyInstaller generates logs that can help with troubleshooting. You may also try running PyInstaller with --debug to see more detailed logs.