# DMA-CFW-Guide
The following guide details instructions on the creation of modified DMA (attack) Firmware based on [pcileech-fpga](https://github.com/ufrisk/pcileech) **version 4.13**. <br />
**Additionally this is intended to be a build off of garagedweller's [UC thread](https://www.unknowncheats.me/forum/anti-cheat-bypass/613135-dma-custom-firmware-guide.html) guide in a more detailed way**<br />

#### 📖Why make this guide?
I know how tedious reading through pages of threads and documentation can be to make some relatively minor changes such as this,
additionally, it doesn't help that there are people intentionally being vague and keeping information secret, or even misleading 
people to push them to buy their +$100 "highly custom undetectable" firmware.

#### 🔎 Definitions
UC
: Unknown Cheats

ACs
: Anti Cheats

DMA
: Direct Memory Access

TLP
: Transaction Layer Packet

DSN
: Device Serial Number

DW
: Double Word


### ⚠️ Disclaimer
- (Don't expect this to work for Vanguard, Faceit, ESEA, or other such ACs that are as 'sophisticated' as they are. <br />
Also, this guide does ___not___ detail how to set up software or change computer settings to accommodate DMA cards)

- It is assumed that the user following the guide has a basic understanding of custom firmware ...  **Finish this list** ... 

- It is not our fault if you brick your computer / DMA card. 

- This guide does not go over how to flash the custom firmware onto your DMA card



### 📑 CONTENTS
1. [Requirements](https://github.com/Silverr12/DMA-FW-Guide#1-requirements)
2. [Gathering the donor information](https://github.com/Silverr12/DMA-FW-Guide#2-gathering-the-donor-information)
3. [Initial Customisation](https://github.com/Silverr12/DMA-FW-Guide#3-initial-customisation)
4. [Vivado Project Generation and Customisation](https://github.com/Silverr12/DMA-FW-Guide#4-vivado-project-generation-and-customisation)
5. [BAR Address & TLP Emulation](https://github.com/Silverr12//DMA-FW-Guide#5-BAR-address-&-tlp-emulation)
6. [Blocks 0x40 and 0x60](https://github.com/Silverr12//DMA-FW-Guide#6-blocks-0x40-and-0x60)

## **1. Requirements**


#### Download all of the following
- [Visual Studio](https://visualstudio.microsoft.com/vs/community/)
- [Xilinx Vivado](https://www.xilinx.com/support/download.html) Will need to make an AMD account to download
- [Pcileech-fpga](https://github.com/ufrisk/pcileech-fpga) Source code for custom firmware
- [Arbor](https://www.mindshare.com/software/Arbor) Will to make an account to download the trial (14 days)




## **2. Gathering the donor information** 
(Using a donor card will help us later on with TLP emulation to communicate with the device to start a driver for legitimacy) <br />
Due to my limited testing and knowledge, I'll be using a network adapter for all examples continuing <br />
<sup>(I welcome any contribution about utilising different hardware for this)</sup>

### Using Arbor
Go into Scan Options under the Local system tab and Press Scan/Rescan, the values selected by default are good enough for us.
Go Into PCI Config and locate your network controller, scroll around in the decode section and take note of the following things:
1. Device ID
2. Vendor ID
3. Revision ID
4. BAR0 (Also click on this value and take note of the sizing value) e.g <br>`Size: 256 bytes (bit 8 is first writable bit; sizing value: FFFF_FF01h)`
5. Subsystem ID
6. DSN(listed as Serial Number Register), just combine the lower and upper DW <sub>**(need to verify)**</sub>

We will still need Arbor later for our 0x40 and 0x60 blocks but it'd be convoluting to explain it here so keep it open

## **3. Initial Customisation**
Once again due to limited knowledge, I'll be focusing on the PCIeSquirrel section of ufrisk's pcileech at the moment, sorry to those using other cards.

### Using Visual Studio
1. Open the PCIeSquirrel folder and head to this file `/PCIeSquirrel/src/pcileech_pcie_cfg_a7.sv`. Within this file use Ctrl+F and search the file for `rw[20]` which should be on line 209 to find the master abort flag/auto-clear status register. Change the accompanying 0 to a 1 along with the accompanying `rw[21]`.

Before

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/358337b4-a238-433c-bc53-0630bec5a17d)


After

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/8814e113-bdd8-43de-81d3-008ef9cfb653)




2. In the same file `pcileech_pcie_cfg_a7.sv` Ctrl+F `rw[127:64]` which should be on line 215 to find your DSN field listed as `rw[127:64]  <= 64'h0000000101000A35;    // cfg_dsn`, insert your Serial Number there as such `rw[127:64]  <= 64'hXXXXXXXXXXXXXXXX;    // cfg_dsn` preserving the 16-character length of the input field, if your DSN is shorter, insert zeroes as seen in the example image<sub>(I think as long as its not the hard code value PCIleech comes with you should be fine as that's what ACs would scan for, please correct me if I'm wrong though.)</sub>

Before

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/788170b0-6e4a-4b87-b1a9-31360abc8575)

After

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/48173453/3943d767-cd13-408f-b1bb-4726749f37ec)


3. Now head to `PCIeSquirrel/src/pcileech_fifo.sv` and Ctrl+F `rw[203]` which should be on line 290 and change the `1'b1;` to `1;b0;` (This will allow us to change the config space bytes later down the line)

Before

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/1443ca9e-91c0-49d4-9979-a403d0f711d0)

After

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/a5aca523-5d14-48d1-9e79-f43adadbb18b)

this being my DSN

4. Go ahead and save all the changes you've made

## **4. Vivado Project Generation and Customisation**
1. Open Vivado and in the top menu, in the search query, search for tcl console and click on it.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/5a3770ad-b821-49c1-bea8-a79684993abc)

The console should now open at the bottom of the application.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/ae96df35-3e46-4f55-8ffd-39b42c8d0972)


2. In the Tcl console, type in `pwd` to see the working directory. It should look something like this `C:/Users/user/AppData/Roaming/Xilinx/Vivado`

3. cd back a few times and then cd to the PCIeSquirrel folder in the pcileech-fpga-4.13 project folder. It should look something like this `C:\Users\user\Desktop\pcileech-fpga-4.13\PCIeSquirrel`. (Desktop is where my project folder is)

4. Once you have PCIeSquirrel dir open, in the Tcl console type in `source vivado_generate_project.tcl -notrace` and wait for it to finish
5. Once the project has been generated, Vivado should automatically open the `pcileech_squirrel.xpr` file.

### Customising within Vivado
1. Once inside Vivado, navigate to the "sources" box and navigate as such `pcileech_squirrel_top` > `i_pcileech_pcie_a7 : pcileech_pcie_a7` then double click on the file with the yellow square labelled `i_pcie_7x_0 : pcie_7x_0`.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/5617a8f8-6d5a-44af-8f88-703bc7d1f101)




2. You should now be in a window called "Re-customize IP", in there, press on the `IDs` tab and enter all the IDs you gathered from your donor board, also note that the "SubSystem Vendor ID" Is just the same as your Vendor ID. _(If your donor board is different from a network adapter you may have to adjust some settings in the "Class Code" section below as well.)_

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/4b0584ec-9dda-4a2a-a5e1-a6e2eb28c6d1)




3. Also go into the "BARs" tab and set the size value you gathered in step 2, note that this is not meant to be the same as your BAR Address
4. Press OK on the bottom right then hit "Generate" on the new window that pops up and wait for it to finish.
5. We will lock the core so that when Vivado synthesises and/or builds our project it will not overwrite some things and to allow us to manually edit some things we could only do through the interface before, to do this, navigate to the "Tcl Console" located in the top right of the bottom box and enter into there `set_property is_managed false [get_files pcie_7x_0.xci]`, (to unlock it in the future for any purposes use `set_property is_managed true [get_files pcie_7x_0.xci]`.)

## **5. BAR Address & TLP Emulation**
1. Back in Visual Studio search for `FFFFF000`, this will come up with a lot of results but we will only be changing

## **6. Blocks 0x40 and 0x60**





### Additional Credits
Ulf Frisk for [pcileech](https://github.com/ufrisk/pcileech) <br />
ekknod for his [custom pcileech config](https://github.com/ekknod/pcileech-wifi)<sub>(I recommend looking into this further if you want to look towards creating firmware to bypass sophisticated ACs)</sub>

