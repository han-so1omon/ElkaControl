Source code and tools for the ElkaControl basestation and Elkaradio USB dongle.

See http://wiki.bitcraze.se/projects:crazyradio:index for more information about Crazyradio and the USB protocol used.

Content:
Firmware: The Elkaradio firmware source code
nrfProg: SPI programmer that uses jtagkey USB adapter
usb_tools: Python scripts to reset and bootload elkaradio from command line
radio_link: Python app to run ElkaControl and manage Elkaradio

Usage:
- Follow http://wiki.bitcraze.se/projects:crazyradio:index for information about
  how to use Elkaradio nrfProg and usb_tools
- Install python 2.7.10 from https://www.python.org/downloads/
  - If on Windows,
		- Make sure to add python to PATH during install
		- Download and install Microsoft Visual C++ Compiler for Python 2.7 from
				https://www.microsoft.com/en-us/download/details.aspx?id=44266
		- Download and install libusb-win32-bin-1.2.6.0 from
				http://sourceforge.net/projects/libusb-win32/files/
		- Download and install Zadig USB driver installer from
				http://zadig.akeo.ie/
				- Plug in Elkaradio device, find Crazyradio device on Zadig, and install libusb-win32 driver
- From the python interpreter, check if you are running a 32 bit or 64 bit Python interpreter

>>> import platform
>>> platform.architecture()
- Run
	pip install --no-index --find-links=./wheels/[sys_type] -r requirements[sys_type].txt to install dependencies
- To use radio_link app:
    Navigate to radio_link folder using 'cd radio_link'
    run app using 'python ./'
