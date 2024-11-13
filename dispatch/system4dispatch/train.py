from .block import Block
from .utilities import Direction, Heading, flip_heading, flip_direction
from enum import Enum


class Train:
    speed = 0
    def __init__(self, name, location:Block, heading:Heading, is_dcc:bool = False, dcc_address:int = None) -> None:
        self.name = str(name)
        self.location = location
        self.heading = heading
        self.direction = Direction.FORWARD
        self.is_dcc = is_dcc
        self.dcc_address = dcc_address

    def set_dcc_address(self, address:int):
        self.dcc_address = address
        
    def update_location(self, location:Block):
        self.location = location
    
    def reverse(self):
        self.direction = flip_direction(self.direction)

    def swap_heading(self):
        self.heading = flip_heading(self.heading)

    def update_speed(self, speed:int):
        self.speed = speed
        if self.is_dcc:
            self.location.set_dcc()
        else:
            self.location.set_dc_speed(self.speed)


    def __str__(self):
        return "Train %s: Heading %s traveling %s at speed %d, on block %s" % (str(self.name), str(self.heading), str(self.direction), self.speed, str(self.location))
