from .block import Block
from enum import Enum

class Heading(Enum):
    WESTBOUND = 0
    EASTBOUND = 1
    SOUTHBOUND = 0
    NORTHBOUND = 1


class Train:
    speed = 0
    def __init__(self, name, location:Block, heading:Heading, is_dcc:bool = False, dcc_address:int = None) -> None:
        self.name = str(name)
        self.location = location
        self.heading = heading
        self.is_dcc = is_dcc
        self.dcc_address = dcc_address

    def set_dcc_address(self, address:int):
        self.dcc_address = address
        
    def update_location(self, location:Block):
        self.location = location
    
    def reverse(self):
        self.heading = (self.heading + 1)%2

    def update_speed(self, speed:int):
        self.speed = speed


    def __str__(self):
        return "Train %s: Heading %s traveling at speed %d, on block %s"
