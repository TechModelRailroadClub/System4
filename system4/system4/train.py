from .block import Block
from enum import Enum

class Direction(Enum):
    Forward = 0
    Reverse = 1

class Train:
    def __init__(self, id:str, location:Block) -> None:
        self.id = id
        self.location = location
        self.speed = 0
        self.direction = Direction.Forward
        

    def __str__(self):
        return 
