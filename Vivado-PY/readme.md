### Automatically changes Basic IDs without touching Vivado

 Before you run the files, edit `generate-project.py`, and `Vivado.py` and change the file location of your project, and uncomment the customisations you want to change.
 
Steps:
1. Put the 3 files in the same directory
2. Run generate-project.py and let this finish
3. Run Vivado.py

once Vivado.py has run. The IDs will have changed. 

I will continue to update this to include more customisations

> [!NOTE]
> This doesn't create the .bin file. you will need to open the xpr file in /PCIeSquirrel/pcileech_squirrel and generate the file within Vivado by pressing Generate Bitstream, or Synthesis.
