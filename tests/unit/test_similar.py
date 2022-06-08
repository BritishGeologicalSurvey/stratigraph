import pytest
from stratigraph.similar import remove_stop_words, Similar, \
        stopped_word, concept_index, remove_surplus_chars


@pytest.fixture
def similar():
    return Similar()


def test_remove_stop():
    s = 'Patrick Burn Formation'
    assert 'Patrick Burn' in remove_stop_words(s)
    assert 'Form' not in remove_stop_words(s)


def test_stopped():
    s = 'Patrick Burn Formation'
    assert 'Formation' in stopped_word(s)


def test_surplus():
    obsolete = 'Keuper Marl And Sandstone [Obsolete Name And Code: Use MMG And SSG]'
    extra = 'Cumbrian Coast Group ( St Bees Evaporites'
    annotated = 'Aegiranum ( Skelton ) Marine Band'
    dashspace = 'Allt - y - Clych Conglomerate'

    assert remove_surplus_chars(obsolete) == 'Keuper Marl And Sandstone'
    assert remove_surplus_chars(extra) == 'Cumbrian Coast Group'
    assert remove_surplus_chars(annotated) == 'Aegiranum Marine Band'
    assert remove_surplus_chars(dashspace) == 'Allt-y-Clych Conglomerate'


def test_stoppable(similar):
    """Add 'Group' to stopwords as we catch a lot more
    However, check afterwards that there wasn't a different word stopped"""
    s = 'Oolite Group'
    assert 'Oolite' in similar.most_similar(s)

    s = 'Oolite Formation'
    assert not similar.most_similar(s)


def test_subset_similar(similar):
    subset = [['Ree Burn',
               'Ree Burn Formation',
               'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/RBN', ''],
              ['Patrick Burn',
               'Patrick Burn Formation',
               'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/PKB', '']]
    similar.match_links = subset
    s = 'Patrick Burn Formation'
    print(similar.most_similar(s))
    assert similar.most_similar(s)


def test_most_similar(similar):
    s = 'Patrick Burn Formation'
    most = similar.most_similar(s)
    assert most
    assert remove_stop_words(s) in most


def test_most_similar_cutoff(similar):
    s = "Pattrick Burn Formation"
    most = similar.most_similar(s)
    assert 'Patrick Burn' in most

    s = "Partick Burn Formation"
    most = similar.most_similar(s)
    assert not most

    most = similar.most_similar(s, cut=0.5)
    assert 'Patrick Burn' in most


def test_concept_index():
    concepts = concept_index()
    keys = [x[0] for x in concepts]
    assert 'Lizard Mica Schists' in keys
