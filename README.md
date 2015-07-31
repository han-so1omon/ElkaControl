Source code and tools for the ElkaControl basestation and Elkaradio USB dongle.

See http://wiki.bitcraze.se/projects:crazyradio:index for more information about Crazyradio and the USB protocol used.

Content:

Firmware: The Elkaradio firmware source code
nrfProg: SPI programmer that uses jtagkey USB adapter
usb_tools: Python scripts to reset and bootload elkaradio from command line
radio_link: Python app to run ElkaControl and manage Elkaradio
Usage:
<<<<<<< HEAD

Follow http://wiki.bitcraze.se/projects:crazyradio:index for information about how to use Elkaradio nrfProg and usb_tools
Install python 2.7.10 from https://www.python.org/downloads/
If on Windows, make sure to add python to PATH during install
If on Windows, download Microsoft Visual C++ Compiler for Python 2.7 from https://www.microsoft.com/en-us/download/details.aspx?id=44266
Run pip install--no-index --find-links=./wheels/ -r requirements.txt to install dependencies
To use radio_link app: Navigate to radio_link folder using 'cd radio_link' run app using 'python ./'
=======
- Follow http://wiki.bitcraze.se/projects:crazyradio:index for information about
  how to use Elkaradio nrfProg and usb_tools
- Install python 2.7.10 from https://www.python.org/downloads/
  - If on Windows, make sure to add python to PATH during install
  - If on Windows, download Microsoft Visual C++ Compiler for Python 2.7 from
     https://www.microsoft.com/en-us/download/details.aspx?id=44266
- Run pip install--no-index --find-links=./wheels/<sys_type> -r requirements.txt to install dependencies
- To use radio_link app:
    Navigate to radio_link folder using 'cd radio_link'
    run app using 'python ./'
>>>>>>> origin/master
