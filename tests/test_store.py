import rdflib
from stratigraph.store import GraphStore

# Could wrap up namespaces neater in the Store


def test_graph():
    g = GraphStore()
    assert g


def test_era():
    g = GraphStore()
    graph = g.in_era('Jurassic')
    assert isinstance(graph, rdflib.Graph)
