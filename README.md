# Hisense DG11L1 AC remote control

This python package implements infrared interface and code generation for 
Hisense DG11L1 AC remote control based on results of the reverse engineering 
explained in `resources/hisense_ir.ipynb`.


## Installation

```bash
pip install git+https://github.com/jon-alamo/hisense-ac-remote-dg11l1.git
```

## Usage

### Interface
The interface mode its only implemented and tested to work with Broadlink's 
rm4-mini device.

```python
from dg11l1 import interface
from dg11l1 import features

device_ip = '192.168.1.20'
device = interface.get_device(device_ip)
interface.send_remote_action(
    device=device, 
    fan_mode=features.FanModes.auto, 
    mode=features.Modes.heat, 
    temperature=20
)
```

### Code generation
The code generation mode is used to generate the raw IR codes for the remote 
control.

```python
from dg11l1 import features

off_code = features.get_remote_action_message(
    fan_mode=features.FanModes.auto, 
    mode=features.Modes.off, 
    temperature=20
)
ifeel_code = features.get_remote_action_message(ifeel_temp=19)
```


