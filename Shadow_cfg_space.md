## Shadow_cfg_space
This section of the guide details how to utilise Pcileech's `pcileech_cfgspace.coe` to customise your firmware without the constraints of Xilinx Vivado

This section of the guide also assumes the reader has read through the main part of the guide, without it you may not understand some steps

Firslty we'll need to convert our donor device's configuration space to a format thats valid for our .coe file, this can be done using 2 ways, I'll be covering it using the easier method

1. Using telescan, save a copy of your donor device's values to a .tlscan file. This can then be converted using this handy [.tlscan to .coe script](https://github.com/Rakeshmonkee/DMA/blob/main/.tlscan%20to%20.coe/telescan_to_coe.py) (instructions for it are in the same repo)

2. In the file `src/pcileech_fifo.sv`, change `rw[203]     <= 1'b1; // CFGTLP ZERO DATA` to -> `1'b0;`. Additionally if you've already changed `rw[20]` and potentially `rw[21]` in `cfg_a7` in the main section of the guide, you'll want to change those back to 0
   
3. Copy the converted file into your `pcileech_cfgspace.coe`. There are some values you may need to change for it to function on your card, main one is to convert your BAR(s) from the address to the sizing (still in the cfgspace.coe file not the vivado gui, though I recommend using it to see what your bar with your specific size **should** look like), also apply the same rules regarding payload/data sizes as in the main part of the guide.
   
4. After the two files are changed and saved, proceed to generate your Vivado project, inside which we'll be changing just the Vendor & Device IDs in the gui and nothing else. Take care to select "Global" in your synthesis options (as seen in the picture)
   ![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/d997c1e7-ba9b-47e6-b0fb-5a31ee2cf4f8)

5. Lock the ip core you just generated and proceed into the `pcie_7x_0_core_top` file, in there change both `EXT_CFG_CAP_PTR` & `EXT_CFG_XP_CAP_PTR` to 01 as seen in the picture, or better yet to 0A if you're proceeding with the writemask step below, keep in mind you will need to manually fill the required values below the area you've set the shadow cfg to take over from.  <br />
   ![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/ec79c104-783f-4e56-b82c-2a3dca66b189)

> [!NOTE]
> The 01 we set for these variables changes where the shadow cfg will take over from in the configuration space, this number we set can be calculated by taking the hex value of the block you want to start from, converting it to decimal, dividing by 4 then converting back to hex. Reference image is below

![image](https://github.com/user-attachments/assets/5d897c5b-b0bd-4626-9424-cda7f0b43a28)


## Writemask
One drawback of using the shadowcfg by itself is that it will automatically set all the values set by it to RO or Read-Only, meaning that other sources will not be able to write to those registers which isn't normally seen on regular devices and can be detected, this is why we will employ the use of pcileech's writemask.

1. Go back to the `pcileech_fifo.sv` file and change `rw[206]     <= 1'b0;  // CFGTLP PCIE WRITE ENABLE` to -> `1'b1;`

2. Utilising a talented individual's script here [writemask.it](https://github.com/Simonrak/writemask.it), you can with the help of the .coe file you generated in the previous section of the guide make a ready-to-go writemask file which you will want to replace your old `ip/pcileech_cfgspace_writemask.coe` with.

3. Generate bitstream using either the console+file or pressing "Generate Bitstream" on the left, wait for it to finish and you're done.

> [!TIP]
> Some instances of "tiny pcie algo" can be solved by changing the `.cfg_force_mps` parameter in the core top file to match your `DEV_CAP_MAX_PAYLOAD_SUPPORTED`, which when set too low can cause the tiny algo

### Credits: <br/>
[@kilmu1337](https://github.com/kilmu1337) and his writeup [here](https://github.com/kilmu1337/DMA-FIRMWARE/blob/main/DMA%20FIRMWARE.md)<br/>
[@Simonrak](https://github.com/Simonrak) for his .coe to writemask script<br/>
(Show some love to both of their efforts)
