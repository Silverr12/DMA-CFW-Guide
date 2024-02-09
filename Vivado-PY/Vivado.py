
#Made with <3 by RakeshMonkee

# Change File Path to the path of your pcie_7x_0_core_top.v File
# Make sure pcileech_squirrel.srcs/sources_1/ip/pcie_7x_0/source/pcie_7x_0_core_top.v is on the end
file_path = "C:/Users/user/Desktop/Vivado-Test/pcileech-fpga-4.13/PCIeSquirrel/pcileech_squirrel/pcileech_squirrel.srcs/sources_1/ip/pcie_7x_0/source/pcie_7x_0_core_top.v"
with open(file_path, 'r') as file:
    verilog_contents = file.read()

# Replace F's with your Values
VendorID = "16'hFFFF"
DeviceID = "16'hFFFF"
RevisionID = "8'hFF"
SubsystemID = "16'hFFFF"
SubsystemVendorID = "16'hFFFF"

#uncomment ClassCode and ClassCode Verilog_contents if you want to change Class Code aswell. Only do if you know what you are doing
#ClassCode = "24'h060000"

# Leave all these Values
verilog_contents = verilog_contents.replace("16'h10EF", f"{VendorID}")
verilog_contents = verilog_contents.replace("16'h0666", f"{DeviceID}")
verilog_contents = verilog_contents.replace("8'h02", f"{RevisionID}")
verilog_contents = verilog_contents.replace("16'h10EE", f"{SubsystemVendorID}")
verilog_contents = verilog_contents.replace("16'h0007", f"{SubsystemID}")
#verilog_contents = verilog_contents.replace("24'h020000", f"{ClassCode}")


with open(file_path, 'w') as file:
    file.write(verilog_contents)