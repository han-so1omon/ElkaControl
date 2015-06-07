import os, platform, serial.tools.list_ports

eradio_port = None

if platform.system() == 'Linux':
    if not os.path.exists('/etc/udev/rules.d/99-crazyradio.rules'):
        with open('/tmp/99-crazyradio.rules', 'w+') as outf:
            outf.write('SUBSYSTEM=="usb", ATTRS{idVendor}=="1915",\
                    ATTRS{idProduct}=="7777", MODE="0664",\
                    GROUP="plugdev", SYMLINK+="elkaradio"')
        os.system('sudo mv /tmp/99-crazyradio.rules /etc/udev/rules.d')
        #FIXME change once GUI implemented
        # os.system('gksu mv /tmp/99-crazyradio.rules /etc/udev/rules.d')
    eradio_port = '/dev/elkaradio'
elif platform.system() == 'Windows':
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Bitcraze' in p[1]:
            #FIXME where are COM ports in Windows?
            eradio_port = '/dev' + target
        else:
            raise ElkaradioNotFound
