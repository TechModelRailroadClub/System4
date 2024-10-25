import pydot
import pyolcb
from .block import Block, BlockAdjacency
from .turnout import Turnout
import re


def _parse_comment(comment: str):
    # Format ADDRESS:ALIAS:INDEX
    comment_split = comment.split(':')
    if comment_split[1] == "":
        comment_split[1] = None
    return {
        "address": pyolcb.Address(comment_split[0], comment_split[1]),
        "index": int(comment_split[2])
    }


def _parse_edge_comment(comment: str):
    return _parse_comment(comment)


def _parse_node_comment(comment: str):
    comment_split = comment.split(':')
    return_val = {}
    if len(comment_split) < 3:
        return_val["is_turnout"] = False
        return return_val
    return_val = _parse_comment(comment) | {"is_turnout": True}
    if len(comment_split) > 3:
        return_val["routes"] = []
        for route in comment_split[3:]:
            route_endpoints = route.split('->')
            return_val["routes"] = (route_endpoints[0], route_endpoints[1])
    return return_val


class Layout:
    blocks = {}
    turnouts = {}
    block_adjacency = {}
    layout_config = {}
    pyolcb_interface = None

    def __init__(self, filename: str, pyolcb_interface: pyolcb.Node) -> None:
        graph = pydot.graph_from_dot_file(filename)[0]

        self.graph = graph
        self.pyolcb_interface = pyolcb_interface

        self.layout_config['turnouts'] = {}
        self.layout_config['block_breaks'] = {}

        for node in self.graph.get_nodes():
            name = node.get_name()
            label = node.get_label()
            id = node.get_name()
            if not isinstance(id, int):
                id = int(re.search(r'\d+', id).group())
            parsed = _parse_node_comment(node.get_comment())
            if name[0] in ['t', 'T'] and name[1:].is_digit() and parsed["is_turnout"] and id not in self.turnouts:
                self.turnouts[int(name[1:])] = Turnout(id, label)
                self.turnouts[int(name[1:])].set_turnoutcard(
                    parsed["address"], parsed["index"])
                self.turnouts[int(name[1:])].set_pyolcb_interface(
                    self.pyolcb_interface)
                self.layout_config['turnouts'][name] = {
                    'pos': node.get_pos(), 'label': label}
            else:
                self.layout_config['block_breaks'][name] = {
                    'pos': node.get_pos(), 'label': label}

        self.layout_config['blocks'] = {}

        for edge in self.graph.get_edges():
            id = edge.get_id()
            if not isinstance(id, int):
                id = int(re.search(r'\d+', id).group())
            label = edge.get_label()
            if id not in self.blocks:
                if label is None or label == "":
                    label = str(id)
                self.blocks[id] = Block(id, label)
                parsed = _parse_edge_comment(edge.get_comment())
                self.blocks[id].set_blockcard(
                    parsed["address"], parsed["index"])
                self.blocks[id].set_pyolcb_interface(self.pyolcb_interface)
                self.blocks[id].turn_off()
                self.block_adjacency[id] = {}
                
            self.layout_config['blocks'][str(edge.get_id())] = {
                'label': label, 'source': edge.get_source(),
                'destination': edge.get_destination()}

        # Fill in block adjacency
        #    CONTINUOUS: Connected, same wiring
        #    DISCONNECTED: Not connected
        #    DISCONTINUOUS: Connected, opposite wiring
        for i in self.graph.get_edges():
            for j in self.graph.get_edges():
                if i.get_destination() == j.get_source():
                    self.block_adjacency[i.get_id(
                    )][j.get_id()] = BlockAdjacency.CONTINUOUS
                elif i.get_destination() == j.get_destination() or i.get_source() == j.get_source():
                    self.block_adjacency[i.get_id()][j.get_id(
                    )] = BlockAdjacency.DISCONTINUOUS
                else:
                    self.block_adjacency[i.get_id()][j.get_id(
                    )] = BlockAdjacency.DISCONNECTED

        # Check no block loops back on itself
        for i in self.blocks:
            if self.block_adjacency[i][i] == -1:
                raise Exception("Reversing loop!")

        for i in self.turnouts:
            self.turnouts[i].set_through()

    def get_layout_state(self):
        layout_state = {}
        layout_state['turnouts'] = {}
        for i in self.turnouts:
            layout_state['turnouts'][i] = {
                "route": self.turnouts[i].get_route()}

        layout_state['blocks'] = {}
        for i in self.blocks:
            layout_state['blocks'][i] = {
                "occupied": self.blocks[i].get_occupied(),
                "signal": self.blocks[i].get_signal(),
                "reversed": self.blocks[i].get_reversed()}

        return layout_state

    def get_layout_config(self):
        return self.layout_config
    
    def get_layout_dot(self):
        return self.graph.to_string()
