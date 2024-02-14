
#Made with <3 by RakeshMonkee

#Make sure to uncomment the customisations you want to change

# Change File Path to the path of your pcie_7x_0_core_top.v File
# Make sure pcileech_squirrel.srcs/sources_1/ip/pcie_7x_0/source/pcie_7x_0_core_top.v is on the end
file_path = "C:/Users/user/Desktop/Vivado-Test/pcileech-fpga-4.13/PCIeSquirrel/pcileech_squirrel/pcileech_squirrel.srcs/sources_1/ip/pcie_7x_0/source/pcie_7x_0_core_top.v"
with open(file_path, 'r') as file:
    verilog_contents = file.read()

#InputvendorID: str = str(input("VendorID: "))[:4]
#InputDeviceID: str = str(input("DevicdID: "))[:4]
#InputRevisionID: str = str(input("RevisionID: "))[:2]
##InputSubsystemID: str = str(input("SubsystemID: "))[:4]
#InputSubsystemVendorID: str = str(input("SubsystemVendorID: "))[:4]
#InputHeaderTypeID: str = str(input("Header Type: "))[:2]
#InputInterupPinID: str = str(input("Interup Pin: "))[:2]
#InputCapabilitesPtrID: str = str(input("Capabilites Ptr: "))[:2]

#VendorID = f"16'h{InputvendorID}"
#DeviceID = f"16'h{InputDeviceID}"
#RevisionID = f"8'h{InputRevisionID}"
#SubsystemID = f"16'h{InputSubsystemID}"
#SubsystemVendorID = f"16'{InputSubsystemVendorID}"
#HeaderTypeID = f"HEADER_TYPE = 8'h{InputHeaderTypeID}"
#CapabitiesPtrID = f"CAPABILITIES_PTR = 8'h{InputCapabilitesPtrID}"
#InteruptPinID = f"INTERRUPT_PIN = 8'{InputInteruptPinID}"

#uncomment ClassCode and ClassCode Verilog_contents if you want to change Class Code aswell. Only do if you know what you are doing
#ClassCode = "24'h060000"

# Leave all these Values
#verilog_contents = verilog_contents.replace("16'10EF", f"{VendorID}")
#verilog_contents = verilog_contents.replace("16'h0666", f"{DeviceID}")
#verilog_contents = verilog_contents.replace("8'h02", f"{RevisionID}")
#verilog_contents = verilog_contents.replace("16'h10EE", f"{SubsystemVendorID}")
#verilog_contents = verilog_contents.replace("16'h0007", f"{SubsystemID}")
#verilog_contents = verilog_contents.replace("HEADER_TYPE = 8'h00", f"{HeaderTypeID})
#verilog_contents = verilog_contents.replace("CAPABILITIES_PTR = 8'h40", f"{CapabitiesPtrID})
#verilog_contents = verilog_contents.replace("INTERRUPT_PIN = 8'h1", f"{InteruptPinID})
#verilog_contents = verilog_contents.replace("24'h020000", f"{ClassCode}")


with open(file_path, 'w') as file:
    file.write(verilog_contents)