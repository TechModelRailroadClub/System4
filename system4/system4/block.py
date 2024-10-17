import pyolcb

class Block:
    before = []
    after = []
    dcc = True
    reversed = False
    occupied = False
    blockcard = None
    blockcard_index = None
    def __init__(self, id:str) -> None:
        self.id = id
    def add_block_before(self, block):
        if not block in self.before:
            self.before.append(block)
    def add_block_after(self, block):
        if not block in self.after:
            self.after.append(block)
    def set_blockcard(self, blockcard:pyolcb.Address, index:int = 0):
        self.blockcard = blockcard
        self.blockcard_index = index

    def set_occupied(self):
        self.occupied = True
    
    def set_unoccupied(self):
        self.occupied = False

    def get_occupied(self):
        return self.occupied
    
    def send_datagram(self, source_node:pyolcb.Node, payload:int = 0):
        # payload = [request response x 1][update speed x 1][dcc enabled x 1][reversed x 1][index x 4][speed x 8]
        if self.blockcard is None:
            raise Exception("No physical blockcard attached!")
        payload = payload | ( int(self.reversed) << 12) | ( int(self.dcc) << 13) | self.blockcard_index << 8

        datagram = pyolcb.Datagram(pyolcb.utilities.process_bytes(2,payload), source_node, self.blockcard)
        source_node.send(datagram)
        return datagram

    def set_dc_speed(self, speed:int, source_node:pyolcb.Node):
        if speed < 0:
            speed = -speed
            self.reversed = True
                    
        if speed > 0x11:
            speed = 0x11

        self.dcc = False
        
        payload = speed
        return self.send_datagram(source_node, payload)
        
    def set_dcc(self, source_node:pyolcb.Node):
        self.dcc = True
        self.send_datagram(source_node)
    
    def set_forward(self, source_node:pyolcb.Node):
        self.reversed = False
        self.send_datagram(source_node)

    def set_reverse(self, source_node:pyolcb.Node):
        self.reversed = True
        self.send_datagram(source_node)

    def request_status(self,source_node:pyolcb.Node):
        self.send_datagram(source_node, 0x8000)

        
    