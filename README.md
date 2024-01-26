# DMA-CFW-Guide
The following guide details instructions on the creation of modified DMA (attack) Firmware based on [pcileech-fpga](https://github.com/ufrisk/pcileech) **version 4.13**. <br />
**Additionally this is intended to be a build-off of garagedweller's [Unknown Cheats thread](https://www.unknowncheats.me/forum/anti-cheat-bypass/613135-dma-custom-firmware-guide.html) guide in a more detailed way**<br />
> [!TIP]
> Video going over steps 1-4: https://www.youtube.com/watch?v=qOPTxYYw63E&ab_channel=RakeshMonkee


#### 📖Why make this guide?
I don't like that there are people intentionally being vague, keeping information secret, or even misleading people to drive
them away from being able to make their own firmware so that they end up buying 100s of dollars worth of custom firmware from
other providers with no way to guarantee quality (I've seen "custom" paid firmware where they've only changed basic IDs lol)

#### 🔎 Definitions
__ACs__
: Anti Cheats

__DMA__
: Direct Memory Access

__TLP__
: Transaction Layer Packet

__DSN__
: Device Serial Number

__DW__
: Double Word | DWORD

__Donor card__
: A card that will be used to get IDs and will not be used on your main PC (Eg. PCIE Wifi card)

### ⚠️ Disclaimer
- (___Don't___ expect this to work for Vanguard, Faceit or ESEA in the guide's current state. <br />

- This guide does ___not___ detail how to set up software or change computer settings to accommodate DMA cards)

- It is assumed that the user following the guide has a basic understanding of custom firmware and so on...

- If you don't understand a single part of this guide, this guide is not for you as you will likely brick your card. Your best and safest bet is to buy a paid CFW making sure at the very least they have TLP emulation and hope for the best it is a 1:1.


### 📑 CONTENTS
1. [Requirements](https://github.com/Silverr12/DMA-FW-Guide#1-requirements)
2. [Gathering the donor information](https://github.com/Silverr12/DMA-FW-Guide#2-gathering-the-donor-information)
3. [Initial Customisation](https://github.com/Silverr12/DMA-FW-Guide#3-initial-customisation)
4. [Vivado Project Customisation](https://github.com/Silverr12/DMA-FW-Guide#4-vivado-project-customisation)
5. [Other Config Space Changes](https://github.com/Silverr12/DMA-CFW-Guide#5-other-config-space-changes)
6. [TLP Emulation](https://github.com/Silverr12/DMA-CFW-Guide#6-tlp-emulation)
7. [Building and Flashing](https://github.com/Silverr12/DMA-CFW-Guide#7-building-and-flashing-only-for-squirrel)

## **1. Requirements**


#### Download all of the following
- [Visual Studio](https://visualstudio.microsoft.com/vs/community/)
- [Xilinx Vivado](https://www.xilinx.com/support/download.html) Will need to make an AMD account to download
- [Pcileech-fpga](https://github.com/ufrisk/pcileech-fpga) Source code for custom firmware
- [Arbor](https://www.mindshare.com/software/Arbor) Will need to make an account to download the trial (14 days)




## **2. Gathering the donor information** 
(Using a donor card will help us later on with TLP emulation to communicate with the device to start a driver for legitimacy) <br />
Due to my limited testing and knowledge, I'll be using a network adapter for all examples continuing <br />
<sup>(I welcome any contribution about utilising different hardware for this)</sup>

It is suggested to use a cheap piece of hardware to get the IDs and then throw it out. These are used to emulate the DMA card. **So don't get the IDs of any existing hardware in your computer and plug them into the firmware. ACs will detect 2 of the same IDs and flag it** 

### Using Arbor
Go into Scan Options under the Local system tab and Press Scan/Rescan, the values selected by default are good enough for us.
Go Into PCI Config and locate your network controller, scroll around in the decode section and take note of the following things:

#### All IDs shown below are mine and might not be the same for you


1. Device ID

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/8baec3fe-c4bd-478e-9f95-d262804d6f67)


2. Vendor ID

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/39c7de6d-d8db-4744-b0a0-ddeca0dfd7d7)


3. Revision ID (will show as RevID)

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/c2374ea7-ca9c-47b7-8a8d-4ceff5dffe3b)


4. BAR0 Sizing Value(1/2/3/4/5 too if you have them)

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/19239179-057a-4ed5-a79f-45cf242787a5)

Click on the square it's in to see the sizing info

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/59a08249-1ce3-49ae-ac98-00e9909ca8e3)

My size is 16kb so record that

5. Subsystem ID

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/94522a95-70bd-4336-8e38-58c0839e38ad)



6. DSN(listed as Serial Number Register)

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/595ae3e2-4cd8-4b3d-bcfa-cf6a59f289d5)
> [!NOTE]
> If the Device Serial Number Capability Structure is not shown for your device, make a randomized string of byte-valid characters or 0 it out completely, but that may look a bit suspicious 
> <sub>(I think as long as its not the hard code value PCIleech comes with you should be fine since that's what ACs would scan for, please correct me if I'm wrong though.)</sub>

Combine your lower and upper DSN registers for our DSN configuration in step 3

For example, these are my values:

Serial Number Register (Lower DW): `68 4C E0 00` <br />
Serial Number Register (Upper DW): `01 00 00 00`<br />

Combine yours in the same format:

Lower DW + Upper DW = `68 4C E0 00 01 00 00 00`


7. We will still need Arbor later for our 0x40 and 0x60 blocks but it'd be convoluting to explain it here so keep it open

## **3. Initial Customisation**
Once again due to limited knowledge, I'll be focusing on the PCIeSquirrel section of pcileech at the moment, sorry to those using other firmware.

### Using Vivado
1. Open Vivado and in the top menu, in the search query, search for tcl console and click on it.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/5a3770ad-b821-49c1-bea8-a79684993abc)

The console should now open at the bottom of the application.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/ae96df35-3e46-4f55-8ffd-39b42c8d0972)


2. In the Tcl console, type in `pwd` to see the working directory. It should look something like this `C:/Users/user/AppData/Roaming/Xilinx/Vivado`

3. cd back a few times and then cd to the PCIeSquirrel folder in the pcileech-fpga-4.13 project folder. It should look something like this `C:\Users\user\Desktop\pcileech-fpga-4.13\PCIeSquirrel`. (Desktop is where my project folder is)

4. Once you have PCIeSquirrel dir open, in the Tcl console type in `source vivado_generate_project.tcl -notrace` and wait for it to finish
5. Once the project has been generated, Vivado should automatically open the `pcileech_squirrel.xpr` file. Keep it open on the side for a bit.

### Using Visual Studio
1. Open the PCIeSquirrel folder and head to this file `/PCIeSquirrel/src/pcileech_pcie_cfg_a7.sv`. Within this file use Ctrl+F and search the file for `rw[20]` which should be on line 209 to find the master abort flag/auto-clear status register. Change the accompanying 0 to a 1 along with the accompanying `rw[21]`.

Before

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/358337b4-a238-433c-bc53-0630bec5a17d)


After

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/8814e113-bdd8-43de-81d3-008ef9cfb653)




2. In the same file `pcileech_pcie_cfg_a7.sv` Ctrl+F `rw[127:64]` which should be on line 215 to find your DSN field listed as `rw[127:64]  <= 64'h0000000101000A35;    // cfg_dsn`, insert your Serial Number there as such `rw[127:64]  <= 64'hXXXXXXXXXXXXXXXX;    // cfg_dsn` preserving the 16-character length of the input field, if your DSN is shorter, insert zeroes as seen in the example image

Before

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/788170b0-6e4a-4b87-b1a9-31360abc8575)

After

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/0e230d17-c649-46a1-93fd-469534f0145b)


this being my DSN

if your donor card didn't have a DSN, yours should look like

`rw[127:64]  <= 64'h0000000000000000;    // +008: cfg_dsn`

4. Go ahead and save all the changes you've made

## **4. Vivado Project Customisation**
1. Once inside Vivado, navigate to the "sources" box and navigate as such `pcileech_squirrel_top` > `i_pcileech_pcie_a7 : pcileech_pcie_a7` then double click on the file with the yellow square labelled `i_pcie_7x_0 : pcie_7x_0`.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/5617a8f8-6d5a-44af-8f88-703bc7d1f101)

2. You should now be in a window called "Re-customize IP", in there, press on the `IDs` tab and enter all the IDs you gathered from your donor board, also note that the "SubSystem Vendor ID" Is just the same as your Vendor ID. _(If your donor board is different from a network adapter you may have to adjust some settings in the "Class Code" section below as well.)_

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/4b0584ec-9dda-4a2a-a5e1-a6e2eb28c6d1)

To check the class code of your donor card go back to Arbor > scan if needed, else > PCI config > set PCI view to Linear. Your card should be highlighted in green. There will also be a column header called **Class**. Match that with your card.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/24131586-03d6-4b70-9000-16448a4d8944)

3. Also go into the "BARs" tab and set the size value you gathered in step 2, note that the Hex Value shown is not meant to be the same as your bar address. You cannot edit this value.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/1942fa3c-71cf-4466-a9a6-a33b5b38e54d)

the size of my bar was 16kb so 16kb is what you set it as

If the size unit is different change the size unit to accommodate the unit of the bar size



4. Press OK on the bottom right then hit "Generate" on the new window that pops up and wait for it to finish.
5. We will lock the core so that when Vivado synthesises and/or builds our project it will not overwrite some things and allow us to edit some things manually we could only do through the interface before, to do this, navigate to the "Tcl Console" located in the top right of the bottom box and enter into there `set_property is_managed false [get_files pcie_7x_0.xci]`, (to unlock it in the future for any purposes use `set_property is_managed true [get_files pcie_7x_0.xci]`.)


---
# **steps 5 and 6** are still in development <sub>(as we are still researching this)</sub>





## **5. Other Config Space Changes**
1. Decide whether you want to modify your config space in the `configspace.coe` file, which:
   - Has a higher probability of (user) error
   - Is less time-consuming  <br />
- **or** in the Vivado IP core, which:
   - Requires more effort
   - Is easier to grasp

**I will first explain how to make the changes in the Vivado IP core editor. If you would instead like to make your changes in the configspace.coe file please scroll down to the appropriate section.**

### For Vivado configspace edit
  1. In Vivado, navigate to `pcie_7x_0_core_top` as shown in the image, and use the magnifying glass in the top left of the text editor to search for these different lines to match them to your donor card

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/c018b760-cb8f-4c08-9efc-e5a3cdd8ed8d)

- Here is a list of variable names in the Vivado IP core config correlating to values we have seen changed when dumping paid CFW that you could change to match your donor cards. Not in any particular order, there is: <br />
  - 0x00 `CLASS_CODE` (easier to do this one in the UI)
  - 0x40 `PM_CAP_VERSION`, `PM_CAP_D1SUPPORT`,`PM_CAP_AUXCURRENT`, `PM_CSR_NOSOFTRST`
  - 0x50 `MSI_CAP_64_BIT_ADDR_CAPABLE`, 
  - 0x60 `PCIE_CAP_DEVICE_PORT_TYPE`, `DEV_CAP_MAX_PAYLOAD_SUPPORTED`, `DEV_CAP_EXT_TAG_SUPPORTED`, `DEV_CAP_ENDPOINT_L0S_LATENCY`, `DEV_CAP_ENDPOINT_L1_LATENCY`, `LINK_CAP_ASPM_SUPPORT`, `LINK_CAP_MAX_LINK_SPEED`, `LINK_CAP_MAX_LINK_WIDTH`
  - 0x90 `LINK_CTRL2_TARGET_LINK_SPEED` <br />
- Fields that can be changed in different files (don't know specifics yet)  <br />
  - 0x40 `cfg_pmcsr_powerstate`
  - 0x60 `corr_err_reporting_en`, `non_fatal_err_reporting_en`, `fatal_err_reporting_en`, `no_snoop_en`
  - 0x90 `Link Status2: Current De-emphasis` (I have not been able to find a single reference to deemph in link status2, nor any other config for this structure, your best bet is modifying this one in the .coe file)

### For configspace.coe file manual edit
> [!IMPORTANT]
> You are matching the bytes by **capability** & **structure**, *not* by **block**, for example, Vendor ID is a structure, whereas MSI is a capability that is made up of many structures and can be located in different blocks on different pieces of hardware

1. In Visual Studio, head to `/src/pcileech_fifo.sv` and Ctrl+F `rw[203]` which should be on line 290 and change the `1'b1;` to `1;b0;` (This will allow us to change the config space bytes)

Before

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/1443ca9e-91c0-49d4-9979-a403d0f711d0)

After

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/a5aca523-5d14-48d1-9e79-f43adadbb18b)

- In comparison with a paid custom firmware versus pcileech default, we have recorded changes in the following bytes (grouped by dword, 1 indicates a change, 0 indicates no change)
  - 0x00 `SKIP-IDS 00000100 01100000 00000000` 
  - 0x40 `11110000 00000001 00000000 00000000` 
  - 0x50 `00100000 11111001 00000000 00000000` 
  - 0x60 `00100000 00000111 00000101 00001101` 
  - 0x90 `00010001 00000000 00000000 00000000` <br />

  
## **6. TLP Emulation**
**Making a guide for this might even need a repo of its own, for now, see [ekknod's bar controller config](https://github.com/ekknod/pcileech-wifi/blob/main/PCIeSquirrel/src/pcileech_tlps128_bar_controller.sv) from line 803 for an example**

---


## **7. Building and Flashing**
> [!CAUTION]
> **It is not our fault if you brick your computer / DMA card with bad firmware (It shouldn't happen anyway if you follow the steps correctly).**<br />

 - Run `source vivado_build.tcl -notrace` in the tcl console to generate the file you'll need to flash onto your card<br />
 - You'll find the file in `pcileech_squirrel/pcileech_squirrel.runs/impl_1` named "pchileech_squirrel_top.bin"<br />
 - Follow the steps on the [official LambdaConcept guide for flashing](https://docs.lambdaconcept.com/screamer/programming.html) **<sub>REMINDER: ONLY FOR SQUIRREL</sub>**

### Flashing troubleshooting
If you mess up your CFW and your game PC won't fully "boot", be because of bios hang or other reasons, you *may* be able to flash new firmware onto it from your second computer if the card is still powered (indicated by the green lights). If your run a DMA card speed test on your second computer and the DMA card isn't recognised (doesn't matter if the rest of the speed test goes through or not), I'm 90% sure it's dead, if your first computer won't stay powered on, you have to buy a PCIe riser that will allow you to power your DMA card without it communicating **(EXTREMELY NOT RECOMMENDED: if a riser is unavailable you can hotplug the dma card in after your computers fully booted then flash the card, be warned however as this can corrupt your motherboard's bios, and there's a chance you may not be able to repair it)**

### Additional Credits
Ulf Frisk for [pcileech](https://github.com/ufrisk/pcileech) <br />
ekknod for his [custom pcileech config](https://github.com/ekknod/pcileech-wifi)<sub>(You could use this as a base to start off of as well!)</sub>






End note:<br />
Don't be like this guy<br />
![:(](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/cf881e80-1139-4641-99c2-325b24bc162a)
