# qdxcat

A Python 3 package for working with the [QDX tranceiver from QRP Labs](http://qrp-labs.com/qdx).

The QDX serial port is auto-detected (tested on Ubuntu 20.04 and Raspberry Pi OS buster) by default, or it can be manually specified.

Auto-detect the serial port:
```
import qdxcat
qdx = qdxcat.QDX()
```

Specify a serial port:
```
import qdxcat
qdx = qdxcat.QDX(port = '/dev/ttyUSB0')
```

Disable auto detect, specify a serial port later:
```
import qdxcat
qdx = qdxcat.QDX(detect = False)
qdx.set_port('/dev/ttyUSB0')
```

Perform auto detect later:
```
import qdxcat
qdx = qdxcat.QDX(detect = False)
qdx.detect()
```

### CAT Commands

The package includes get and set functions for all documented CAT commands (some commands seem not to be working with firmware v1.03). Check out the example.py file in the repo.

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
