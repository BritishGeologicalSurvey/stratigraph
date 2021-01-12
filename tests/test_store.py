import rdflib
from stratigraph.store import GraphStore

# Could wrap up namespaces neater in the Store


def test_graph():
    g = GraphStore()
    assert g


def test_graph_by_era():
    g = GraphStore()
    #test selection for Jurassic
    graphJ = g.graph_by_era('http://data.bgs.ac.uk/id/Geochronology/Division/J')
    assert isinstance(graphJ, rdflib.Graph)
    formation_labels_J = [str(graphJ.label(s)) for s in graphJ.subjects()]  # noqa: E501
    assert 'Kimmeridge Clay Formation' in formation_labels_J

