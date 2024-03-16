# DMA-CFW-Guide
本指南详细地说明了如何制作自定义DMA固件。基于 [pcileech-fpga](https://github.com/ufrisk/pcileech-fpga) **4.13版本**。<br />


如果你知道自己在做什么，请查阅 [Vivado 定制](https://github.com/Silverr12/DMA-CFW-Guide/blob/main/Possible%20Vivado%20Customisations.md)

> [!TIP]
> 1-4步的视频教学: https://www.youtube.com/watch?v=qOPTxYYw63E&ab_channel=RakeshMonkee


#### 📖为什么要制作本指南?
我不喜欢有人故意含糊其辞，对这些方法保密，甚至误导人们，让他们无法制作自己的固件，然后玩家就会花费100+刀去买那些没有质量保证的固件。

#### 设备兼容性
本指南使用松鼠DMA. 如果你用的不是这个DMA，请根据 pcileech-fpga 库中有的项目来制作。

- 35T: Squirrel

- 75T: EnigmaX1

- 100T: ZDMA


#### 🔎下个定义
__ACs__
: 反作弊程序

__DMA__
: 直接存储器访问

__TLP__
: PCIe事务层

__DSN__
: 设备序列号

__DW__
: 双字(四个字节为一双字) | DWORD

__Donor card__
: 就像一个料板，获取它的信息并赋予给你的DMA，来伪装成正常的设备 (举例: PCIE插槽的WIFI网卡)

__FPGA__
: 现场可编程逻辑门阵列

### ⚠️ 免责声明
- (___不要___ 期盼本指南目前的操作能够绕过 Vanguard，Faceit，或是 ESEA. <br />

- This guide does ___not___ detail how to set up software or change computer settings to accommodate DMA cards)

- I recognise that there are a lot of methods that skirt around the current detection vectors but this guide covers trying to emulate a legitimate device 1:1 because this is the most future-proof/least likely to be detected in the future from my current understanding.

- If you don't understand a single part of this guide，this guide is not for you as you will likely brick your card. Your best and safest bet is to buy a paid CFW making sure at the very least they have TLP emulation and hope for the best that it's a 1 of 1.


### 📑 目录
1. [Requirements](https://github.com/Silverr12/DMA-FW-Guide#1-requirements)
2. [Gathering the donor information](https://github.com/Silverr12/DMA-FW-Guide#2-gathering-the-donor-information)
3. [Initial Customisation](https://github.com/Silverr12/DMA-FW-Guide#3-initial-customisation)
4. [Vivado Project Customisation](https://github.com/Silverr12/DMA-FW-Guide#4-vivado-project-customisation)
5. [Other Config Space Changes](https://github.com/Silverr12/DMA-CFW-Guide#5-other-config-space-changes)
6. [TLP Emulation](https://github.com/Silverr12/DMA-CFW-Guide#6-tlp-emulation)
7. [Building，Flashing & Testing](https://github.com/Silverr12/DMA-CFW-Guide#7-building-flashing--testing)

## **1. Requirements**
#### Hardware
 - A donor card (explained below)
 - A DMA card of course 

#### Software
- A text editor，[Visual Studio](https://visualstudio.microsoft.com/vs/community/) is used in this guide.
- [Xilinx Vivado](https://www.xilinx.com/support/download.html) Will need to make an AMD account to download
- [Pcileech-fpga](https://github.com/ufrisk/pcileech-fpga) Source code for custom firmware
- [Arbor](https://www.mindshare.com/software/Arbor) Will need to make an account to download the trial (14 days) <br />
<sub>The trial can be extended by deleting the appropriate folder in your registry editor，I don't think I can tell you more than that though.</sub>
- Alternative to Arbor，[Telescan PE](https://www.teledynelecroy.com/protocolanalyzer/pci-express/telescan-pe-software/resources/analysis-software)，this one's very similar and completely free but requires a manual review of your registration which can take a bit.

## **2. Gathering the donor information** 
(Using a donor card will help us later on with TLP emulation to communicate with the device to start a driver for legitimacy) <br />
Due to my limited testing and knowledge，I'll be using a network adapter for all examples continuing <br />
<sup>(If you know what you are doing and understand the nuances，you can skip buying a donor card entirely，but for first timers I highly recommend this，way better to know you have a guaranteed-to-work product by spending $20 then sit on an alt for 2 weeks waiting for a delay ban to test your firmware)</sup>

It is suggested to use a cheap piece of hardware to get the IDs and then throw it out. These are used to emulate the DMA card. **So don't get the IDs of any existing hardware in your computer and plug them into the firmware. ACs will most likely in the future if not already，detect 2 devices with 1:1 IDs and flag them** 

### Using Arbor
Go into Scan Options under the Local system tab and Press Scan/Rescan，the values selected by default are good enough for us.
Go Into PCI Config and locate your network controller，scroll around in the decode section，and take note of the following things:

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
> If the Device Serial Number Capability Structure is not shown for your device，make a randomized string of byte-valid characters，0 it out completely，or disable the capability altogether.

Combine your lower and upper DSN registers for our DSN configuration in step 3

For example，these are my values:

Serial Number Register (Lower DW): `68 4C E0 00` <br />
Serial Number Register (Upper DW): `01 00 00 00`<br />

Combine yours in the same format:

Lower DW + Upper DW = `68 4C E0 00 01 00 00 00`


7. We will still need Arbor later for our 0x40 and 0x60 blocks but it'd be convoluting to explain it here so keep it open

## **3. Initial Customisation**
Once again due to limited knowledge，I'll be focusing on the PCIeSquirrel section of pcileech at the moment，sorry to those using other firmware.


### Using Visual Studio
1. Open the PCIeSquirrel folder and head to this file `/PCIeSquirrel/src/pcileech_pcie_cfg_a7.sv`. Within this file use Ctrl+F and search the file for `rw[20]` which should be on line 209 to find the master abort flag/auto-clear status register. Change the accompanying 0 to a 1 along with the accompanying `rw[21]`.

Before

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/358337b4-a238-433c-bc53-0630bec5a17d)


After

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/8814e113-bdd8-43de-81d3-008ef9cfb653)


Setting `rw[21]` to a 1，allows the DMA card to access the CPU’s memory directly (DMA) or exchange TLPs with peer peripherals (to the extent that the switching entities support that)

2. In the same file `pcileech_pcie_cfg_a7.sv` Ctrl+F `rw[127:64]` which should be on line 215 to find your DSN field listed as `rw[127:64]  <= 64'h0000000101000A35;    // cfg_dsn`，insert your Serial Number there as such `rw[127:64]  <= 64'hXXXXXXXXXXXXXXXX;    // cfg_dsn` preserving the 16-character length of the input field，if your DSN is shorter，insert zeroes as seen in the example image.

Before

![image](https://github.com/Silverr12/DMA-FW-Guide/assets/89455475/788170b0-6e4a-4b87-b1a9-31360abc8575)

After

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/0a6238f3-5691-483d-a9a0-97d972d1c893)


this being my DSN

if your donor card didn't have a DSN，yours should look like

`rw[127:64]  <= 64'h0000000000000000;    // +008: cfg_dsn`

4. Go ahead and save all the changes you've made


### Generating the Vivado files
1. Open Vivado and in the top menu，in the search query，search for tcl console and click on it.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/5a3770ad-b821-49c1-bea8-a79684993abc)

The console should now open at the bottom of the application.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/ae96df35-3e46-4f55-8ffd-39b42c8d0972)


2. In the Tcl console，type in `pwd` to see the working directory. It should look something like this `C:/Users/user/AppData/Roaming/Xilinx/Vivado`

3. cd to the PCIeSquirrel folder in the pcileech-fpga-master project folder. It should look something like this `C:\Users\user\Desktop\pcileech-fpga-master\PCIeSquirrel`. (Desktop is where my project folder is) <sub> If you get an error when trying to cd to your project directory，replace all the '\'s with '/'</sub>

4. Once you have PCIeSquirrel dir open，in the Tcl console type in `source vivado_generate_project.tcl -notrace` and wait for it to finish
5. Once the project has been generated，Vivado should automatically open the `pcileech_squirrel.xpr` file. Keep it open on the side for a bit.

## **4. Vivado Project Customisation**
1. Once inside Vivado，navigate to the "sources" box and navigate as such `pcileech_squirrel_top` > `i_pcileech_pcie_a7 : pcileech_pcie_a7` then double click on the file with the yellow square labelled `i_pcie_7x_0 : pcie_7x_0`.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/5617a8f8-6d5a-44af-8f88-703bc7d1f101)

2. You should now be in a window called "Re-customize IP"，in there，press on the `IDs` tab and enter all the IDs you gathered from your donor board，also note that the "SubSystem Vendor ID" Is just the same as your Vendor ID. _(If your donor board is different from a network adapter you may have to adjust some settings in the "Class Code" section below as well.)_

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/4b0584ec-9dda-4a2a-a5e1-a6e2eb28c6d1)

To check the class code of your donor card go back to Arbor > scan if needed，else > PCI config > set PCI view to Linear. Your card should be highlighted in green. There will also be a column header called **Class**. Match that with your card.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/24131586-03d6-4b70-9000-16448a4d8944)

3. Also go into the "BARs" tab and set the size value you gathered in step 2，note that the Hex Value shown is not meant to be the same as your bar address. You cannot edit this value.

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/89455475/1942fa3c-71cf-4466-a9a6-a33b5b38e54d)

the size of my bar was 16kb so 16kb is what you set it as

If the size unit is different change the size unit to accommodate the unit of the bar size



4. Press OK on the bottom right then hit "Generate" on the new window that pops up and wait for it to finish.<br />
![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/df292771-63c0-4013-9eaf-bb2c39e52539)

5. We will lock the core so that when Vivado synthesises and/or builds our project it will not overwrite some things and allow us to edit some things manually we could only do through the interface before，to do this，navigate to the "Tcl Console" located in the top right of the bottom box and enter into there `set_property is_managed false [get_files pcie_7x_0.xci]`，(to unlock it in the future for any purposes use `set_property is_managed true [get_files pcie_7x_0.xci]`.)


---
# **Steps 5 and 6** are being actively researched and updated and therefore are not complete or final，proceed with caution





## **5. Other Config Space Changes**

  1. In Vivado，navigate to `pcie_7x_0_core_top` as shown in the image，and use the magnifying glass in the top left of the text editor to search for these different lines to match them to your donor card

![image](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/c018b760-cb8f-4c08-9efc-e5a3cdd8ed8d)

#### - Here is a list of variable names in the manual Vivado IP core config correlating to values we have confirmed to **not** break your firmware that you could change to match your donor cards that we've been able to match by name from Arbor. matched by capability，there is: <br />
  - (PM) `PM_CAP_VERSION`，`PM_CAP_D1SUPPORT`,`PM_CAP_AUXCURRENT`，`PM_CSR_NOSOFTRST`
  - (MSI) `MSI_CAP_64_BIT_ADDR_CAPABLE`，
  - (PCIe) `PCIE_CAP_DEVICE_PORT_TYPE`，`DEV_CAP_MAX_PAYLOAD_SUPPORTED`，`DEV_CAP_EXT_TAG_SUPPORTED`，`DEV_CAP_ENDPOINT_L0S_LATENCY`，`DEV_CAP_ENDPOINT_L1_LATENCY`，`LINK_CAP_ASPM_SUPPORT`，`LINK_CAP_MAX_LINK_SPEED`，`LINK_CAP_MAX_LINK_WIDTH`，`LINK_CTRL2_TARGET_LINK_SPEED`
  - Fields that can be changed in different files or a GUI that I do not yet know about. <br />
    - (PM) `cfg_pmcsr_powerstate`
    - (PCIe) `corr_err_reporting_en`，`non_fatal_err_reporting_en`，`fatal_err_reporting_en`，`no_snoop_en`，`Link Status2: Current De-emphasis`


#### - It is also advised that you change the block locations of the capabilities，this can be done by changing the following variables:
  - Capability NEXT Pointers:`CAPABILITIES_PTR`，`MSI_CAP_NEXTPTR`，`PCIE_CAP_NEXTPTR`，`PM_CAP_NEXTPTR` and
  - Capability Pointers: `MSI_BASE_PTR`，`PCIE_BASE_PTR`，`PM_BASE_PTR`

On default pcileech firmware you can locate: **PM at 0x40，MSI at 0x50，and PCIe at 0x60**，The example will be changing them to **PCIe at 0x40，PM at 0xC8 and MSI at 0xD0**，but you can have them at any location really (e.g PCIe at 0x80，PM at 0xD0 and MSI at 0x90) since our computers can and will jump over the empty blocks，all you have to do is make sure the `NEXTPTR`'s line up to the next capability as explained below and that you take note of the capabilities sizes so they don't try to overlap.
- You need your NEXTPTRs lined up starting from your header at 0x00 and going up in the config blocks，for example:
  - If I were to change my capabilities blocks around to `PCIe: 0x40 | PM: 0xC8 | MSI: 0xD0` I would simply assign their associated `BASE_PTR` variables as such to the same value. Always make to start at or above 0x40 as our header ends just before it and also make sure your base ptrs always end on 0，4，or 8 such as 40，44 68.
  - Secondly，I would also have to have my header capability pointer `CAPABILITIES_PTR` point to 40 (which it is by default) since it's our lowest/first to be read in this case，then the `PCIE_CAP_NEXTPTR` will point to C8，`PM_CAP_NEXTPTR` to D0 and `MSI_CAP_NEXTPTR` to 00 to finalise it out，and always make sure it's in order from top to bottom as if you try to point backward in the config space your firmware will not work. (Extended capabilities such as AER，DSN，LTR，etc also require this configuration if you decide to put them in. But you do not point the regular capabilities into them as they are a separate 'set'，besides that they follow the same pointer format as your regular capabilities.)


> [!IMPORTANT]
> Once you have completed steps 1-5，you **should，with 98% confidence**，be good to go for BE，EAC，and any other anti-cheat that you can think of **that isn't VGK，Faceit or ESEA**
> For them your best bet would be lots of trial and error with emulating different devices，doing odd config space changes，and changing things around in pcileech，many will not reveal their methods unless they want it detected，so you are mostly on your own there unfortunately.

  
## **6. TLP Emulation**
**For now，see [ekknod's bar controller config](https://github.com/ekknod/pcileech-wifi/blob/main/src/pcileech_tlps128_bar_controller.sv) mainly from line 850-896 for an example**

Notes to consider:

- Either some classes of devices do not require drivers or have generic drivers automatically load which in either case bypasses some or all sophisticated ACs (e.g devices that use the same artix-7 chip as your card would.)
 

- You don't need to thoroughly understand any coding language for this as complicated as this may seem，it's going to be just changing certain addresses

1. You have two options for obtaining the register addresses for the device you're emulating，your options are:
- Navigate to this [Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_open-source_wireless_drivers) page that lists open-source/reverse-engineered drivers that you could take values from for your firmware
- Using a program of your choice (Recommend IDA Pro) to reverse engineer the driver for your donor card，you can find the location of the installed driver by navigating to your device in the device manager，going to Properties>Driver>Driver Details，and it should normally be the only .dll file in there. (Mind you intel does **not** release their sources without contractual obligation so good luck if you're adamant about them)

2. (to be done)

3. In Visual Studio head to `/src/pcileech_tlps128_bar_controller.sv` and use the template file in the repo to implement. (soon to come)

4. (to be done，maybe latency/timing checks)


### Resources for TLP Emulation
1. https://fpgaemu.readthedocs.io/en/latest/infrastructure.html
2. https://www.incibe.es/sites/default/files/2023-11/INCIBE-CERT_FIRMWARE_ANALYSIS_SCI_GUIDE_2023_v1.1.pdf
3. https://docs.xilinx.com/v/u/en-US/pcie_blk_plus_ug341
4. https://www.fpga4fun.com/PCI-Express4.html
5. https://www.xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-1



## **7. Building，Flashing & Testing**
> [!CAUTION]
> **There is a good chance that on your first flash if you went about some of the more 'harder' to navigate steps it will mess something up，don't worry，and look at the troubleshooting below.**<br />

1. Run `source vivado_build.tcl -notrace` in the tcl console to generate the file you'll need to flash onto your card<br />
   - You'll find the file in `pcileech_squirrel/pcileech_squirrel.runs/impl_1` named "pchileech_squirrel_top.bin"<br />
2. Follow the steps on the [official LambdaConcept guide for flashing](https://docs.lambdaconcept.com/screamer/programming.html) **<sub>REMINDER: ONLY FOR SQUIRREL</sub>**
3. Run a DMA speed test tool from your second computer <sub>(There is a link and download in the discord server)</sub> to verify your firmware is working and reading as it should be.
4. Dump and compare the config space of your new firmware to the **known** signed pcileech default seen below to see if it's overly similar. You should most definitely be right about some values being the same，you have to think about the fact that apart from the serial number and maybe bar address，the configuration space of one type of (for example) network card is going to be the same across all of them. So as long as your new firmware's configuration space does not closely resemble the default，you have a legitimate device for all the ACs care. GLHF

This is the signature BE supposedly scan for in the config space of the PCIe device:
[More info here](https://dma.lystic.dev/anticheat-evasion/detection-vectors)<br>
     `40: 01 48 03 78 08 00 00 00 05 60 80 00 00 00 00 00`<br />
     `60: 10 00 02 00 e2 8f XX XX XX XX XX XX 12 f4 03 00`<br />
     ("XX" are bytes that they do not care about)

Another form of detection that may or may not be implemented that could be blocking your firmware is reading your device history，this can be cleaned by following [this](https://dma.lystic.dev/anticheat-evasion/clearing-device-history) post.

### Flashing troubleshooting
- If you mess up your CFW and your game PC won't fully "boot"，be because of bios hang or other reasons，you *may* be able to flash new firmware onto it from your second computer if the card is still powered (indicated by the green lights). If you run a DMA card speed test on your second computer and the DMA card isn't recognised (doesn't matter if the rest of the speed test goes through or not)，I'm 90% sure it's dead，if your first computer won't stay powered on，you have to buy a PCIe riser that will allow you to power your DMA card without it communicating **(EXTREMELY NOT RECOMMENDED: if a riser is unavailable you can hotplug the dma card in after your computers fully booted then flash the card，be warned however as this can corrupt your motherboard's bios，and there's a chance you may not be able to repair it)**
- There are flat-out some motherboards that will be incompatible with some firmware，what about them I know 0 about，the safest bet is to clone a device that you know already works on your machine.

### 'Dysfunctional' firmware troubleshooting
- If your speed test prompts something along the lines of `tiny PCIe algorithm`，you have made a mistake somewhere in your capabilities. Your card *will* still function but reads will be slower than they should be which can severely impact performance.
- Changing some functions below acceptable bounds most likely named something including payload/size/speed **can** also slow down the reading speed of your card. The best course of action is to set max read request/payload sizes to 4KB
- Some motherboards will simply be incompatible with some firmware，most reports have been on gigabyte mobos.
- Sometimes your firmware will allow your device to work but cause a massive slowdown then BSOD your computer if it tries to read it with Arbor or Device Manager. Unfortunately，I don't know exactly where you need to go wrong for this to happen so I recommend re-doing your whole firmware. I suggest keeping a stable firmware that works，on your second computer in case this happens.
- Are your changes not saving when making a new .bin file? Try deleting your `pcileech_squirrel.runs` folder and/or also making and working in a new copy of the stock pcileech-fpga folder every new firmware as good practice


### Once you've read through all this,
If you have any questions，problems with your firmware or suggestions，feel free to join my Discord for support.
[![Discord Banner](https://discord.com/api/guilds/1205153997166608394/widget.png?style=banner2)](https://discord.com/invite/reEgerZX3u)


### Additional Credits
Ulf Frisk for [pcileech](https://github.com/ufrisk/pcileech) <br />
Ekknod for his [custom pcileech config](https://github.com/ekknod/pcileech-wifi)<sub>(You could use this as a base to start off of as well!)</sub> <br />
Garagedweller's [Unknown Cheats thread](https://www.unknowncheats.me/forum/anti-cheat-bypass/613135-dma-custom-firmware-guide.html) that inspired me to make this in the first place and whom I credit my interest in this topic to.

### Sponsor this project
If you feel this guide has helped you enough to warrant a monetary donation，feel free to donate here: <br />
USDT/trc20: `1BNVf49u5GMuHg8teDcnexChqzyHB4MB2T` <br />
![usdtaddr](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/36a8a6d6-1edd-4289-96b9-a9003a7c4a26)<br />

LTC: `MMxWW2n5pTbWoY9EakDaTiQ7HKBJy7sxDh`<br />
![ltcaddr](https://github.com/Silverr12/DMA-CFW-Guide/assets/48173453/e243973f-7b84-42a9-b78a-19a7a12aac98)<br />
or just starring the repo helps **immensely** too <3 <br />
<sub>also sponsor the [man who's making this all possible](https://github.com/ufrisk)<br />

