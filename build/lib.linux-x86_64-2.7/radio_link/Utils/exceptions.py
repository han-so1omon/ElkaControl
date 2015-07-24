"""
Author: Eric Solomon
Project: Elka Control
Lab: Alfred Gessow Rotorcraft Center
Package: Utils 
Module: exceptions.py 

Exceptions for Inputs
JoystickNotFound: Used when Joystick has not been found
                  Prompt user to input controller

Exceptions for Elkaradio
ElkaradioNotFound: Used when Elkaradio has not been found
                    Prompt user to connect Elkaradio
LinkEstablished: Used when connect is attempted on a link that is already in
                 place
                 Tell user that eradio is busy
LinkException: Used when there is an error in the communications link. E.g. no
               ack is being received
               End comm, flush queues, and restart link

QueueFullException: Attempted to load too many instructions into out_queue
                    Alert user and continue operating as normal

WrongDataTypeException: Data must be str, tuple, or list type

"""

class JoystickNotFound (Exception):
    """ No Joystick found """ 
    pass

class ElkaradioNotFound (Exception):
    """No Elkaradio found """
    pass

class LinkEstablished (Exception):
    """ Elkaradio link already in place """
    pass

class LinkException(Exception):
    """ Error in communications link """
    pass

class QueueFullException(Exception):
    """ Attempted to load too many instructions into out_queue """
    pass

class WrongDataTypeException(Exception):
    ''' Data must be str, tuple, or list type '''
    pass

class JoystickThreadFinished(Exception):
    ''' Loop break condition is satisfied, so thread stops '''
    pass

class InvalidCommand(Exception):
    ''' Invalid command given to interpreter '''
    pass
