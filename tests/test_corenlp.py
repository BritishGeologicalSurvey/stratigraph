import pytest
from unittest.mock import patch
from requests.exceptions import ConnectionError

from stratigraph.corenlp import entities, tokens

SAMPLE = """The data we provide includes field contect photographs of the sites and the samples that were taken, photographic logs of the drilled rock cores annotated with details of the parts that have been sampled, together with detailed geochemical analyses including XRF, XRD and ICP-MS analyses of acid dissolved samples. The 5 localities are sites where there are published records of fossil plants and paleosols. Late Silurian deposit at Bloomsburg, Pennsylvania; Lower Devonian deposit at Gaspe Bay Quebec; Miiddle Devonian forest at Cairo Quarry New York State; slightly later middle Devonian forest at Gilboa, New York; and late Devonian site at Red Hill Hyner, Pennsylvania.""" # noqa E501

DEBUG_SAMPLE = "Bibliographic reference: Green, D.W. 1992. Bristol and Gloucester region. British Regional Geology. London: HMSO, 1992." # noqa E501


@patch("stratigraph.corenlp.SERVER", "http://localhost:1234")
def test_tokens_exception():
    with pytest.raises(ConnectionError):
         tokens(SAMPLE)

def test_tokens_works():
    result = tokens(SAMPLE)
    assert isinstance(result, dict)
    assert 'sentences' in result

def test_entities():
    entity_doc = entities(SAMPLE)
    assert entity_doc
    assert 'start_char' in entity_doc[0]

    entity_doc = entities('')
    assert entity_doc == []


def test_fullstop_bugfix():
    entity_doc = entities('By J.R. Davies, D. Wilson, I.T. Williamson')
    entity_doc
    names1 = [e['name'] for e in entity_doc]
    entity_doc = entities('By J.R. Davies, D. Wilson, I.T. Williamson.')
    names2 = [e['name'] for e in entity_doc]
    assert names1
    assert names1 == names2
