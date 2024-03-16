> [!CAUTION]注意  
> 如果错误地修改本指南提到的参数，会使你的 DMA 报废。   
> 我已经提醒你了，只要你从你的 Donor card 获取这些参数就不会出错。   
  
如果你认为本指南有错误，请不要吝啬您的 "issue"

下面是你在 Vivado 可以修改的一些参数。你可以使用 Arbor 从你的 Donor card 来获取它们。不是所有的选项我都添加在了下面的名单内，这些只是我修改过的。我无法在 Arbor 找到以下参数 Ext-Capabilities，Ext-Capabilities2，TL Settings，DL & PL Settings，Shared Logic，Core Interface Parameters，并且我也无法在 Arbor 中添加 Debug 选项，目前我还没弄懂上述参数。  

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

DSN Capability:
- DSN Capability
- Change DSN value within `pcileech_pcie_cfg_a7.sv`


Vendor Specific Capability:
- VSEC Capability


Virtual Channel Capability:
- VC Capability
- Reject Snoop Transactions

