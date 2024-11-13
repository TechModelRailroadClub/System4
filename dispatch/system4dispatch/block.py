import pyolcb
from .utilities import Signal
from enum import Enum

class Adjacency(Enum):
    CONTINUOUS = 1
    DISCONNECTED = 0
    DISCONTINUOUS = -1

class Block:
    dcc = True
    reversed = False
    occupied = False
    signal = None
    blockcard = None
    blockcard_index = None
    pyolcb_interface = None
    
    def __init__(self, id:int, name:str=None) -> None:
        self.id = id
        self.name = name

    def __eq__(self, value: object) -> bool:
        return value.id == self.id
    
    def __str__(self) -> str:
        if self.name is None:
            return str(self.id)
        else:
            return self.name

    def set_blockcard(self, blockcard:pyolcb.Address, index:int = 0):
        self.blockcard = blockcard
        self.blockcard_index = index

    def set_pyolcb_interface(self, pyolcb_interface:pyolcb.Node):
        self.pyolcb_interface = pyolcb_interface

    def set_occupied(self):
        self.occupied = True
        self.signal = Signal.OCCUPIED
    
    def set_approach(self):
        self.signal = Signal.APPROACH
        self.occupied = False
    
    def set_clear(self):
        self.occupied = False
        self.signal = Signal.CLEAR

    def get_occupied(self):
        return self.occupied
    
    def get_signal(self):
        return self.signal
    
    def send_datagram(self, payload:int = 0):
        # payload = [0x0][short address x 12b][index x 4b]
        #           [request response x 1b][update speed x 1b]
        #           [dcc enabled x 1b][reversed x 1b][speed x 8b]
        if self.blockcard is None:
            raise Exception("No physical blockcard attached!")
        payload = payload | ( int(self.reversed) << 8) | ( int(self.dcc) << 9) | self.blockcard_index << 12 | self.blockcard.get_alias() << 16

        datagram = pyolcb.Datagram(pyolcb.utilities.process_bytes(4,payload), self.pyolcb_interface, self.blockcard)
        self.pyolcb_interface.send(datagram.as_message_list())
        return datagram

    def set_dc_speed(self, speed:int):
        speed = min(abs(speed), 127)
        self.dcc = False
        payload = speed
        return self.send_datagram(payload)

    def turn_off(self):
        return self.set_dc_speed(0)
        
    def set_dcc(self):
        self.dcc = True
        self.send_datagram()
    
    def set_forward(self):
        self.reversed = False
        self.send_datagram()

    def set_reverse(self):
        self.reversed = True
        self.send_datagram()

    def request_status(self):
        self.send_datagram(0x00000800)
    
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_reversed(self):
        return self.reversed
    
    


        
    