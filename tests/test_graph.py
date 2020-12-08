import os
import rdflib
import networkx as nx
from networkx.classes.function import is_empty, info
from stratigraph.graph import triples, bounds_texts, ttl_to_nx, \
        graph_to_dot


def test_triples():
    entities = [{'name': 'Test', 'url': 'http://data.bgs.ac.uk/id/Test/1'}]
    source = 'http://data.bgs.ac.uk/id/Test/2'
    g = triples(source, entities)
    assert isinstance(g, rdflib.Graph)


def test_bounds_texts():
    mmg = 'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/MMG'
    texts = bounds_texts(mmg)
    print(texts)
    assert(texts[0]['upper'])


def test_ttl_to_nx_empty():
    # Base case with empty graphs
    graph = rdflib.Graph()
    nx_graph = ttl_to_nx(graph=graph)
    assert isinstance(nx_graph, nx.DiGraph)
    assert is_empty(nx_graph)


def test_ttl_to_nx_empty():
    triples = os.path.join(os.path.dirname(__file__), 'fixtures', 'jurassic.ttl')
    graph = rdflib.Graph()
    graph.parse(triples, format='ttl')
    print([s for s in graph.subjects()])
    nx_graph = ttl_to_nx(graph=graph)
    print(info(nx_graph))
    assert not is_empty(nx_graph)
