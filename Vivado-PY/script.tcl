#Made with <3 by RakeshMonkee

source vivado_generate_project.tcl -notrace

#change to your dir, needs to look like dir below
cd C:/Users/user/Desktop/Vivado-Test/pcileech-fpga-4.13/PCIeSquirrel/pcileech_squirrel/pcileech_squirrel.srcs/sources_1/ip/pcie_7x_0

generate_target {all} [get_files pcie_7x_0.xci]

set_property is_managed false [get_files pcie_7x_0.xci]