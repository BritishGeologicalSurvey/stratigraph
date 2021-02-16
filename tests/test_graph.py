import os
import rdflib
import networkx as nx
import networkx.algorithms.isomorphism as iso
from networkx.classes.function import is_empty
from stratigraph.graph import triples, bounds_texts, ttl_to_nx, \
     graph_to_dot


def test_triples():
    entities = [{'name': 'Test', 'url': 'http://data.bgs.ac.uk/id/Test/1'}]
    source = 'http://data.bgs.ac.uk/id/Test/2'
    g = triples(source, entities)
    lst = [s for (s, p, o) in g]
    assert lst
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


def test_ttl_to_nx():
    # Case in which we supply a graph
    triples = os.path.join(os.path.dirname(__file__),
                           'fixtures',
                           'jurassic.ttl')
    graph = rdflib.Graph()
    graph.parse(triples, format='ttl')
    nx_graph = ttl_to_nx(graph=graph)
    assert not is_empty(nx_graph)

    # Case in which we only supply triples, not graph
    nx_graph = ttl_to_nx(triples=triples)
    assert not is_empty(nx_graph)

    # Case in which we include orphaned nodes
    nx_full_graph = ttl_to_nx(triples=triples, orphan_nodes=False)
    assert nx_full_graph.number_of_nodes() < nx_graph.number_of_nodes()

    # Case in which we use the age colour scale
    nx_graph_age = ttl_to_nx(triples=triples, colour_scale='age')
    assert not is_empty(nx_graph_age)

    # Check graphs created with different colour scale are the same if not
    # comparing attributes
    nx_graph_digmap = ttl_to_nx(triples=triples)
    assert nx.is_isomorphic(nx_graph_digmap, nx_graph_age)

    # Check graphs created with different colour scale are different when
    # also comparing attributes
    nm = iso.categorical_node_match('fillcolor', '#EEEEEE')
    assert not nx.is_isomorphic(nx_graph_digmap, nx_graph_age, node_match=nm)


def test_graph_to_dot():
    triples = os.path.join(os.path.dirname(__file__),
                           'fixtures',
                           'jurassic.ttl')
    graph = rdflib.Graph()
    graph.parse(triples, format='ttl')
    # write_dot writes to file path or filehandle
    # read it back in when sending via the API?
    dot = graph_to_dot(graph=graph)
    assert 'data.bgs.ac.uk' in dot
    assert 'id=' in dot
