# qdxcat

Implements CAT control for the  [QRPLabs QDX transceiver](http://qrp-labs.com/qdx).

Serial port interfacing is cross-platform by the use of the pySerial package. The QDX serial port is auto-detected by default.

### Examples

Auto-detect serial port (default):
```
import qdxcat
qdx = qdxcat.QDX()
```

Specify serial port:
```
import qdxcat
qdx = qdxcat.QDX('/dev/ttyXXX')
```

Disable auto-detect, specify serial port later:
```
import qdxcat
qdx = qdxcat.QDX(autodetect = False)
qdx.set_port('/dev/ttyXXX')
```

Perform auto-detect later:
```
import qdxcat
qdx = qdxcat.QDX(autodetect = False)
qdx.autodetect()
```

Get and set frequency:
```
import qdxcat
qdx = qdxcat.QDX()

qdx.get(qdx.VFO_A)
qdx.set(qdx.VFO_A, 7078000)
```

Manage PTT:
```
import qdxcat
qdx = qdxcat.QDX()

# turn ptt on and off manually
qdx.ptt_on()
qdx.ptt_off()

# toggle ptt state
qdx.toggle_ptt()
# transmit something here
qdx.toggle_ptt()
```

See `qdxcat.QDX.COMMANDS` for a full list of supported commands.

### Install

Install the *qdxcat* package and dependencies using *pip*:
```
pip3 install qdxcat
```

**Note:** Linux operating systems may require that a user be added to the *dialout* group to access serial ports without *sudo*. Check if the current user is a member of the *dialout* group using the `groups` terminal command. If *dialout* is not listed, add a user to the group using the following terminal command:

```
sudo usermod -a -G dialout *user*
```

A restart may be required for group changes to take effect.

### Software Beta State

**This software is still under development and should be considered a beta release.**
