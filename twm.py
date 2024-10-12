from computer import Computer
import os, subprocess

class TellWithMe:
    '''
    This class need for communication between computers.
    '''
    def __init__(self): ...

    def send(self, command: str): ...

class TellWithMeScripter(TellWithMe):
    '''
    This class is script creator for TellWithMe.
    '''
    def __init__(self): ...

    def crate_bridge(self): ...
