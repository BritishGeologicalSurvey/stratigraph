"""Test a store with useful data.
Currently depends on having Fuseki locally with fixtures."""

from stratigraph.store import GraphStore


def test_graph_by_era():
    g = GraphStore()

    # Supply a code for now, but better to use a URL?
    # url = 'https://data.bgs.ac.uk/id/Geochronology/Division/J'
    era_code = 'J'
    graph = g.graph_by_era(era_code)
    formation_labels = [str(graph.label(s)) for s in graph.subjects()]  # noqa: E501
    assert 'Kimmeridge Clay Formation' in formation_labels

    graph = g.graph_by_era(era_code, full=True)
    all_labels = [str(graph.label(s)) for s in graph.subjects()]  # noqa: E501

    # There SHOULD be fewer labels in the formation list than the all list
    # Because non-Formations are less likely to have both upper and lower links?
    # Because we haven't text mined enough, or the query is borked, or both?
    assert len(all_labels) > len(formation_labels)
