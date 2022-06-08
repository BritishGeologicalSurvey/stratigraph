"""Test a store with useful data.
Currently depends on having Fuseki locally with fixtures."""

from rdflib.namespace import RDFS

from stratigraph.store import GraphStore
from stratigraph.ns import GEOCHRON


def test_graph_by_era():
    g = GraphStore()

    era_uri = str(GEOCHRON.J)
    graph = g.graph_by_era(era_uri)
    formation_labels = [str(graph.value(s, RDFS.label)) for s in graph.subjects()]  # noqa: E501
    assert 'Kimmeridge Clay Formation' in formation_labels

    graph = g.graph_by_era(era_uri, full=True)
    all_labels = [str(graph.value(s, RDFS.label)) for s in graph.subjects()]  # noqa: E501

    # There should be fewer labels in the formation list than the all list
    assert len(all_labels) > len(formation_labels)


def test_graph_from_code():
    g = GraphStore()
    graph = g.graph_all()
    formation_labels = [str(graph.value(s, RDFS.label)) for s in graph.subjects()]  # noqa: E501
    assert 'Rannoch Formation' in formation_labels

    # TODO implement node distance and check that graph grows
