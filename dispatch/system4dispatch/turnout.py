from enum import Enum
import pyolcb


class Route(Enum):
    THROUGH = 0
    DIVERGING = 1

class Turnout:
    route = Route.THROUGH
    turnoutcard = None
    turnoutcard_index = None
    pyolcb_interface = None
    def __init__(self, id:int, name:str=None) -> None:
        self.id = id
        self.name = name

    def set_turnoutcard(self, turnoutcard:pyolcb.Address, index:int = 0):
        self.turnoutcard = turnoutcard
        self.turnoutcard_index = index

    def set_pyolcb_interface(self, pyolcb_interface:pyolcb.Node):
        self.pyolcb_interface = pyolcb_interface

    def set_route(self, route:Route):
        self.route = route
        if self.turnoutcard is None:
            raise Exception("No physical turnoutcard attached!")
        payload = (int(self.route)) | self.turnoutcard_index << 4 | self.turnoutcard.get_alias() << 8
        datagram = pyolcb.Datagram(pyolcb.utilities.process_bytes(2,payload), self.pyolcb_interface, self.turnoutcard)
        self.pyolcb_interface.send(datagram.as_message_list())
        return self.route
    
    def set_diverging(self):
        return self.set_route(Route.DIVERGING)
    
    def set_through(self):
        return self.set_route(Route.THROUGH)
    
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_state(self):
        return self.route
    
    def get_route(self):
        return self.route



