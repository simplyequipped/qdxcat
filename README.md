# qdx

A Python 3 package for working with the [QDX tranceiver from QRP Labs](http://qrp-labs.com/qdx).

The qdx pacakge default is to auto discover the QDX device when using a Linux system (tested on Ubuntu 20.04). If the QDX cannot be discovered you can specify a serial port by passing the serial port to the qdx.QDX() constructor in your Python script, or by entering the serial port information through the web interface when prompted. Auto discovery can also be disabled by passing the appropraite information to the qdx.QDX() constructor.

Specify the serial port:
```
radio = qdx.QDX(port = '/dev/ttyUSB0')
```

Disable auto discovery:
```
radio = qdx.QDX(discovery = False)
```

### CAT Commands

The package includes get and set functions for all documented CAT commands (some commands seem not to be working with firmware v1.03). Check out the example.py file included in the repo for an example of working with the CAT functions.

### Web Interface

The package also includes a web interface for connecting to the QDX as well as changing some settings (commands that do not work in firmware v1.03 are not supported on the web interface for now). The web interface is a simple flask web app with support for a waitress server as well as the flask development-only server.

To start the waitress server using a specific host and port:
```
sudo python3
>>> import qdx
>>> qdx.serve(host='localhost', port=8080)
```

To start the waitress server accepting all incoming requests (host='0.0.0.0', default port=5000):
```
sudo python3
>>> import qdx
>>> qdx.serve_all()
```

To start the waitress server accepting all incoming requests with a custom port:
```
sudo python3
>>> import qdx
>>> qdx.serve_all(port=8080)
```

To start the flask development server accepting all incoming requests with a custom port:
```
sudo python3
>>> import qdx
>>> qdx.server.dev_server(host='0.0.0.0', port=8080)
```

Note that the package will need to be added to your PATH environmental variable, or you will need to run the above commands in the directory containing the qdx package.

### Dependencies

```
pip3 install pyserial, waitress

```
Note that sudo may be required to access the serial port. If so, be sure to run the above pip3 install using sudo as well.

### Software Alpha State

**This software is still under development and should be considered an alpha release.**
