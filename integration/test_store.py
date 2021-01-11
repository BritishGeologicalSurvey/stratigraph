"""Test a store with useful data.
Currently depends on having Fuseki locally with fixtures."""

from stratigraph.store import GraphStore
from stratigraph.ns import GEOCHRON, LEXICON


def test_graph_by_era():
    g = GraphStore()

    era_uri = str(GEOCHRON.J)
    graph = g.graph_by_era(era_uri)
    formation_labels = [str(graph.label(s)) for s in graph.subjects()]  # noqa: E501
    assert 'Kimmeridge Clay Formation' in formation_labels

    graph = g.graph_by_era(era_uri, full=True)
    all_labels = [str(graph.label(s)) for s in graph.subjects()]  # noqa: E501

    # There SHOULD be fewer labels in the formation list than the all list
    assert len(all_labels) > len(formation_labels)


def test_graph_from_code():
    g = GraphStore()
    code_uri = str(LEXICON.BROM)
    graph = g.graph_from_code(code_uri)
    formation_labels = [str(graph.label(s)) for s in graph.subjects()]  # noqa: E501
    assert 'Rannoch Formation' in formation_labels

    # TODO implement node distance and check that graph grows
