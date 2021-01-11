import rdflib
from stratigraph.store import GraphStore

# Could wrap up namespaces neater in the Store


def test_graph():
    g = GraphStore()
    assert g


def test_era():
    g = GraphStore()
    graphJ = g.graph_by_era('http://data.bgs.ac.uk/id/Geochronology/J')
    assert isinstance(graphJ, rdflib.Graph)
    graphC = g.graph_by_era('http://data.bgs.ac.uk/id/Geochronology/C')
    # assert Jurassic and Carboniferous graphs contain different triples
    assert len(graphJ - graphC) == 0
    graphNull = g.graph_by_era('http://data.bgs.ac.uk/id/Geochronology/does-not-exist')
    assert len(graphNull) == 0
    
