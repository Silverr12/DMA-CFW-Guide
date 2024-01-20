# DMA-FW-Guide
The following guide details instructions on the creation of modified DMA (attack) Firmware based on [pcileech-fpga](https://github.com/ufrisk/pcileech) version 4.13. <br />
**Additionally this is intended to be a build off of garagedweller's [UC thread](https://www.unknowncheats.me/forum/anti-cheat-bypass/613135-dma-custom-firmware-guide.html) guide in a more detailed way**<br />

#### 📖Why make this guide?
I know how tedious reading through pages of threads and documentation can be to make some relatively minor changes such as this,
additionally, it doesn't help that there are people intentionally being vague and keeping information secret, or even misleading 
people to push them to buy their +$100 "highly custom undetectable" firmware.

### ⚠️ Disclaimer
- (Don't expect this to work for Vanguard, Faceit, ESEA, or other such sophisticated ACs as they are much more 'intrusive'. <br />
Also, this guide does ___not___ detail how to set up software or change computer settings to accommodate DMA cards)

- It is assumed that the user following the guide has a basic understanding of custom firmware ...  **Finish this list** ... 

- It is not our fault if you brick your computer / DMA card. 

- This guide does not go over on how to flash the custom firmware onto your DMA card



### 📑 CONTENTS
1. [Requirements](https://github.com/Silverr12/DMA-FW-Guide#1-requirements)
2. [Gathering the donor information](https://github.com/Silverr12/DMA-FW-Guide#2-gathering-the-donor-information)
3. [Initial Customisation](https://github.com/Silverr12/DMA-FW-Guide#3-initial-customisation)
4. [Vivado Project Generation and Customisation](https://github.com/Silverr12/DMA-FW-Guide#4-vivado-project-generation-and-customisation)

## **1. Requirements**


#### Download all of the following
- [Visual Studio](https://visualstudio.microsoft.com/vs/community/)
- [Xilinx Vivado](https://www.xilinx.com/support/download.html)
- [Pcileech-fpga](https://github.com/ufrisk/pcileech-fpga) source code for custom firmware
- [RWEverything](http://rweverything.com/download/)





## **2. Gathering the donor information** 
(Using a donor card will help us later on with TLP emulation to communicate with the device to start a driver for legitimacy) <br />
Due to my limited testing and knowledge, I'll be using a network adapter for all examples continuing <br />
<sup>(I welcome any contribution about utilising different hardware for this)</sup>

### Using RWEverything
<sup> I will eventually update the guide to utilise Arbor which provides more concise information
Press PCI Devices in the top left and navigate the list to find your donor card
Once in here, under "Summary" on the right hand side, take note of the:
1. Device & Vendor ID, under Summary it will display for example as _0x2G4H5302_, disregarding the 0x, the first 4 letters/numbers are your Device ID, and the other 4 the Vendor ID.
2. Revision ID
3. BAR1
4. Subsystem ID, but only the first 4 letters/numbers once again as the other 4 is a duplicate of our Vendor ID
5. Either take a picture of the block of bytes underneath the dropdown or save the dump as a file
6. DSN(Device Serial Number) if you see it in there, for me it was on the box of the donor card

## **3. Initial Customisation**
Once again due to limited knowledge I'll be focusing on the PCIeSquirrel section of ufrisk's pcileech at the moment, sorry to those using other cards.

### Using Visual Studio
1. Open the PCIeSquirrel folder from Pcileech with Visual Studio and use Ctrl+Shift+F to search the solution for `rw[20]` to find the master abort flag/auto-clear status register, it should be listed in `pcileech_pcie_cfg_a7.sv` on line 209, now change the accompanying 0 to a 1 along with the accompanying one on `rw[21]`.
2. Now in the same file go to `rw[127:64]` to find your DSN field listed as `rw[127:64]  <= 64'h0000000101000A35;    // cfg_dsn`, insert your Serial Number there as such `rw[127:64]  <= 64'h0000000xxxxxxxx;    // cfg_dsn` <sub>(I don't think it has to be exact as long as its not the hard coded value that pcileech comes with, as that is what AC's would scan for, please correct me if im wrong though.)</sub>
3. Use the search function once again to search for `bar_0` which should be located in `pcie_7x_0.xci`, change the accompanying default `>FFFFF000<` to the bar1 address you gathered in step 1, don't mind that its your 'bar1' that you're pasting into bar0, RWEverything shifted them all up by one.

## **4. Vivado Project Generation and Customisation**
1. Press your windows key and type 'tcl shell' and open it, then use cd to point to your project folder, this is easily done by going to your project folder, clicking on the file address bar and copying the file address (before cding you *may* have to reverse the slashes in the address.)
2. Now type in `source vivado_generate_project.tcl -notrace` and wait for it to finish.











### Additional Credits
Ulf Frisk for [pcileech](https://github.com/ufrisk/pcileech) <br />
ekknod for his [custom pcileech config](https://github.com/ekknod/pcileech-wifi)<sub>(I recommend looking into this further if you want to look towards creating firmware to bypass sophisticated ACs)</sub>

