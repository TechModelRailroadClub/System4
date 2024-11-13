from enum import Enum

class Heading(Enum):
    NORTHBOUND = 0
    EASTBOUND = 1
    SOUTHBOUND = 2
    WESTBOUND = 3

def flip_heading(heading:Heading):
    return (heading + 2) % 4

class Direction(Enum):
    FORWARD = 0
    BACKWARD = 1

def flip_direction(direction:Direction):
    return (direction + 1) % 2

class Signal(Enum):
    CLEAR = 0
    OCCUPIED = 1
    APPROACH = 2