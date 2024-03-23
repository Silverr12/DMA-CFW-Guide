## Shadow_cfg_space
This section of the guide details how to utilise Pcileech's `pcileech_cfgspace.coe` to customise your firmware without the constraints of Xilinx Vivado

This section of the guide also assumes the reader has read through the main part of the guide, without it you may not understand some steps

Firslty we'll need to convert our donor device's configuration space to a format thats valid for our .coe file, this can be done using 2 ways, I'll be covering it using the easier method

1. Using telescan, save a copy of your donor device's values to a .tlscan file. This can then be converted using this handy [.tlscan to .coe script](https://github.com/Rakeshmonkee/DMA/blob/main/.tlscan%20to%20.coe/telescan_to_coe.py) (instructions for it are in the same repo)

2. In the file `src/pcileech_fifo.sv`, change `rw[203]     <= 1'b1;                        //       CFGTLP ZERO DATA` to -> `1'b0;`. Additionally change the `rw[20]      <= 1;                       //       CFGSPACE_STATUS_REGISTER_AUTO_CLEAR [master abort flag]` as well as seen in the main part of the guide
   
3. Copy the converted file into your `pcileech_cfgspace.coe`. There are some values you may need to change for it to function on your card, main one is to convert your BAR(s) from the address to the sizing as can be seen in the main part of the guide, also apply the same rules regarding payload/data sizes.
   
4. After the two files are changed and saved, proceed to generate your Vivado project, inside which we'll be changing just the Vendor & Device IDs in the gui and nothing else. Take care to select "Global" in your synthesis options (as seen in the picture)
   ![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/d997c1e7-ba9b-47e6-b0fb-5a31ee2cf4f8)

5. Lock the ip core you just generated and proceed into the `pcie_7x_0_core_top` file, in there change both `EXT_CFG_CAP_PTR` & `EXT_CFG_XP_CAP_PTR` to 01 (as seen in the picture) <br />
   ![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/ec79c104-783f-4e56-b82c-2a3dca66b189)

7. Generate bitstream using either the console+file or pressing "Generate Bitstream" on the left, wait for it to finish and you're done.


> [!TIP]
> Some instances of "tiny pcie algo" can be solved by changing the `.cfg_force_mps` parameter in the core top file to match your `DEV_CAP_MAX_PAYLOAD_SUPPORTED`, which when set too low can cause the tiny algo


Credit: @kilmu1337
