import graphviz
import pyolcb

class Layout:
    blocks = {}
    turnouts = {}
    def __init__(self, filename:str) -> None:
        source = graphviz.Source.from_file(filename)
        graph = graphviz.Graph()

        source_lines = str(source).splitlines()
        # Remove 'digraph tree {'
        source_lines.pop(0)
        # Remove the closing brackets '}'
        source_lines.pop(-1)
        # Append the nodes to body
        graph.body += source_lines

        self.graph = graph
    