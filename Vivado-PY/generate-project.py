import os
import subprocess

#Made with <3 by RakeshMonkee

script_dir = os.path.dirname(os.path.abspath(__file__))

# Change to DIr of your xilinx vivado installation
vivado_path = "D:/Xilinx/Vivado/2023.2/bin/vivado.bat"


tcl_script_name = "script.tcl"


tcl_script_path = os.path.join(script_dir, tcl_script_name)

# Change to Dir of your project
project_dir = "C:/Users/user/Desktop/Vivado-Test/pcileech-fpga-4.13/PCIeSquirrel"


command = [vivado_path, "-mode", "tcl", "-source", tcl_script_path, "-notrace"]

subprocess.run(command, cwd=project_dir)