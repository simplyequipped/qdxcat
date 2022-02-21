# qdx

A Python 3 package for working with the [QDX tranceiver from QRP Labs](http://qrp-labs.com/qdx).

The qdx pacakge default is to auto discover the QDX device when using a Linux system (tested on Ubuntu 20.04 and Raspberry Pi OS buster). If the QDX cannot be discovered you can specify a serial port by passing the serial port to the qdx.QDX() constructor. Auto discovery can also be disabled by passing the appropraite information to the qdx.QDX() constructor.

Auto discovery:
```
import qdx
radio = qdx.QDX()
```

Specify a serial port:
```
import qdx
radio = qdx.QDX(port = '/dev/ttyUSB0')
```

Disable auto discovery, specify a serial port later:
```
import qdx
radio = qdx.QDX(discovery = False)
radio.set_port('/dev/ttyUSB0')
```

Disable auto discovery, auto discover later:
```
import qdx
radio = qdx.QDX(discovery = False)
radio.discover()
```

### CAT Commands

The package includes get and set functions for all documented CAT commands (some commands seem not to be working with firmware v1.03). Check out the example.py file included in the repo for an example of working with the CAT functions as well as the QDX.command() utility function.

### Install

Package installation is handled by the setup script. In addition to the typical Python install, the setup script can also add the user to the 'dialout' group to enable serial port access without using sudo. Configuration of the 'dialout' group is optional and is handled by prompting the user during setup.

Clone this repo and install the package:
```
git clone https://github.com/simplyequipped/qdx
cd qdx
python3 setup.py install
```

The only dependency is the Python serial package which can be installed manually if needed:
```
pip3 install pyserial
```

### Software Alpha State

**This software is still under development and should be considered an alpha release. Significant changes are likely.**
