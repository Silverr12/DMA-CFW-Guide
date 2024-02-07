> [!CAUTION]
> Anything mentioned here that **isn't in** the main readme has not been tested, you are on your own here. Don't create an issue asking for help with this. it's not our fault if you don't listen and brick your card changing the wrong values.

If you believe something is wrong, open an issue

Some Possible Customisations in Vivado. You get the values from Arbor from your Donor Card. Not all Tabs have been added as these are the functions, that I have changed. I cannot find anything about Ext-Capabilities, Ext-Capabilities2, TL Settings, DL & PL Settings, Shared Logic, Core Interface Parameters, and Add Debug Options in Arbor and am not sure about these.



IDs:
- Vendor ID 
- Device ID 
- Revision ID 
- Subsystem Vendor ID 
- Subsystem ID 


Class Code:
- Base Class Menu 
- Base Class Value
- Sub Class Interface Menu
- Sub Class Value
- Cardbus CIS Pointer


Bars (0):
- Type
- Size Unit
- Size Value
- Prefetchable


Device Capabilities Register:
- Max Payload Size
- Extended Tag Field
- Extended Tag Default
- Phantom Functions
- Acceptable L0s Latency
- Acceptable L1 Latency


Link Status Register:
- Slot Clock Configuration


Legacy Interrupt Settings:
- Interrupt PIN


MSI Capabilities:
- MSI Capability Structure
- 64 bit Address Structure


MSIx Capabilities:
-- will need to calculate table and PBA Offset


Power Management Registers:
- Device Specific Initialization
- D1 Support
 -D2 Support


PME SUPPORT:
- D0
- D1
- D2
- D3hot
- D3cold
- No Soft Reset
