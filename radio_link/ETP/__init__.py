"""
Elka Transfer Protocol

Packets are 20 bytes long.

Packet format is as follows:
    {3B: Header, 6B: Control inputs, 11B: Zeros}

Packets contain the following header:
    x, 255, 255
    where x = {3: pilot inputs, 2: gains}

Packets contain the following data elements:
    roll, pitch, thrust, and yaw
These are determined by the right horizontal, right vertical,
left vertical, and left horizontal axes on an external joystick input.
Values range from 0-4000

PID are as follows:
    roll (p,i,d)
    pitch (p,i,d)
    yaw (d)

"""
