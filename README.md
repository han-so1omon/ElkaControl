Source code and tools for the ElkaControl basestation and Elkaradio USB dongle.

See http://wiki.bitcraze.se/projects:crazyradio:index for more information about Crazyradio and the USB protocol used.

Content:
Firmware: The Elkaradio firmware source code
nrfProg: SPI programmer that uses jtagkey USB adapter
usb_tools: Python scripts to reset and bootload Elkaradio from command line
radio_link: Python app to run ElkaControl and manage Elkaradio

Usage:
- Follow http://wiki.bitcraze.se/projects:crazyradio:index for information about
  how to use Elkaradio nrfProg and usb_tools

- Install python 2.7.10 from https://www.python.org/downloads/
  - If on Windows,
    - Make sure to add python to PATH during install
    - Download and install Microsoft Visual C++ Compiler for Python 2.7 from
          https://www.microsoft.com/en-us/download/details.aspx?id=44266

- Set up Elkaradio USB
  - If on Windows,
    - Download and install libusb-win32-bin-1.2.6.0 from
        http://sourceforge.net/projects/libusb-win32/files/
    - Download and install Zadig USB driver installer from
        http://zadig.akeo.ie/
    - Plug in Elkaradio device, find Crazyradio device on Zadig, and install libusb-win32 driver
  - If on Linux,
    - Add yourself as the owner of the ElkaControl directory
        chmod 4755 /path/to/ElkaControl
        chown -R yourusername /path/to/ElkaControl
    - Check if there is a plugdev group
        groups
    - If not, add a plugdev group
        sudo groupadd plugdev
    - Add yourself to the plugdev group
        sudo usermod -a -G plugdev <username>
    - Add the following to the /etc/udev/rules.d/ directory as 73-eradio.rules 
        SUBSYSTEM=="usb",ATTRS{idVendor}=="1915",ATTRS{idProduct}=="7777"
        MODE="0664",SYMLINK="eradio",GROUP="plugdev"

- From the python interpreter, check if you are running a 32 bit or 64 bit Python interpreter

>>> import platform
>>> platform.architecture()

- Run
    pip install --no-index --find-links=./wheels/[sys_type] -r requirements[sys_type].txt to install dependencies

- If you are having trouble with dependencies try running
    pip install [package]
  and making sure that the version is at least that specified in the
  requirements.txt file

- Dependency installations may require administrative/superuser privileges

- Certain dependencies are available throught the apt- utility on Ubuntu

- To use radio_link app:
  - Navigate to radio_link folder from home folder using 
    'cd /path/to/ElkaControl/radio_link'
  - Run app using 'python ./'
