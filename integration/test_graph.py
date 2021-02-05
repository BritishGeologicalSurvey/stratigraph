import rdflib
from stratigraph.graph import link_entities, bounds_links, bounds_texts


def test_link_entities():
    text = 'A sentence that contains a Patrick Burn Formation named entity'
    link_list = link_entities(text)
    assert isinstance(link_list, list)
    assert 'url' in link_list[0]


def test_bounds_links():
    pkb = 'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/PKB'
    texts = bounds_texts(pkb)
    g = bounds_links(pkb, texts)
    assert isinstance(g, rdflib.Graph)
