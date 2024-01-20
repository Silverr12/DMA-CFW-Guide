# DMA-FW-Guide
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

## **1. Requirements**


#### Download all of the following
- [Visual Studio](https://visualstudio.microsoft.com/vs/community/)
- [Xilinx Vivado](https://www.xilinx.com/support/download.html)
- [Pcileech-fpga](https://github.com/ufrisk/pcileech-fpga) Source code for custom firmware
- [Arbor]([http://rweverything.com/download/](https://www.mindshare.com/software/Arbor)) You have to make an account to download the trial




## **2. Gathering the donor information** 
(Using a donor card will help us later on with TLP emulation to communicate with the device to start a driver for legitimacy) <br />
Due to my limited testing and knowledge, I'll be using a network adapter for all examples continuing <br />
<sup>(I welcome any contribution about utilising different hardware for this)</sup>

### Using Arbor
Go into Scan Options and Press Scan/Rescan, the values selected by default are good enough for us.
Go Into PCI Config and locate your network controller, scroll around in the decode section and take note of the following things:
1. Device ID
2. Vendor ID
3. Revision ID
4. BAR0
5. Subsystem ID
6. DSN(listed as Serial Number Register), just combine the lower and upper DW <sub>**(need to verify)**</sub>

We will still need Arbor later for our 0x40 and 0x60 blocks but it'd be convoluting to explain it in here so keep it open

## **3. Initial Customisation**
Once again due to limited knowledge, I'll be focusing on the PCIeSquirrel section of ufrisk's pcileech at the moment, sorry to those using other cards.

### Using Visual Studio
1. Open the PCIeSquirrel folder from Pcileech with Visual Studio and use Ctrl+Shift+F to search the solution for `rw[20]` to find the master abort flag/auto-clear status register, it should be listed in `pcileech_pcie_cfg_a7.sv` on line 209, now change the accompanying 0 to a 1 along with the accompanying one on `rw[21]`.
2. Now in the same file go to `rw[127:64]` to find your DSN field listed as `rw[127:64]  <= 64'h0000000101000A35;    // cfg_dsn`, insert your Serial Number there as such `rw[127:64]  <= 64'hXXXXXXXXXXXXXXXX;    // cfg_dsn` <sub>(I don't think it has to be exact as long as its not the hard coded value that pcileech comes with, as that is what AC's would scan for, please correct me if I'm wrong though.)</sub>
3. Use the search function once again to search for `rw[203]` which will be located in `pcileech_fifo.sv`, change the `1'b1;` to `1'b0;` (This will allow us to change the config space bytes later down the line)
4. Go ahead and save all the changes you've made

## **4. Vivado Project Generation and Customisation**
1. Press your Windows key and type 'tcl shell' and open it, then use cd to point to your project folder, this is easily done by going to your project folder, clicking on the file address bar and copying the file address (before cding you *may* have to reverse the slashes in the address.)
2. Now type in `source vivado_generate_project.tcl -notrace` and wait for it to finish.

### Customising within Vivado
1. Navigate to the newly created "pcileech_squirrel" folder made by Vivado and open the .xpr file. (the first open may take a bit longer than expected)
2. Once inside Vivado, navigate to the "sources" box and navigate as such `pcileech_squirrel_top` > `i_pcileech_pcie_a7 : pcileech_pcie_a7` then double click on the file with the yellow square labelled `i_pcie_7x_0 : pcie_7x_0`.
3. You should now be in a window called "Re-customize IP", in there, press on the `IDs` tab and enter all the IDs you gathered from your donor board, also note that the "SubSystem Vendor ID" Is just the same as your Vendor ID. _(If your donor board is different from a network adapter you may have to adjust some settings in the "Class Code" section below as well.)_
4. Press OK on the bottom right then hit "Generate" on the new window that pops up and wait for it to finish.
5. We will lock the core so that when Vivado synthesises and/or builds our project it will not overwrite some things and to allow us to manually edit some things we could only do through the interface before, to do this, navigate to the "Tcl Console" located in the top right of the bottom box and enter into there `set_property is_managed false [get_files pcie_7x_0.xci]`, to unlock it in the future for any purposes use `set_property is_managed true [get_files pcie_7x_0.xci]`.

## **5. BAR Address & Blocks 0x40 and 0x60**


## **6. TLP Emulation**




### Additional Credits
Ulf Frisk for [pcileech](https://github.com/ufrisk/pcileech) <br />
ekknod for his [custom pcileech config](https://github.com/ekknod/pcileech-wifi)<sub>(I recommend looking into this further if you want to look towards creating firmware to bypass sophisticated ACs)</sub>

