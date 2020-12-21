import os
from unittest.mock import MagicMock
import rdflib
from fastapi.testclient import TestClient
from stratigraph.api import app, load_graph

client = TestClient(app)


class MockGraph(MagicMock):
    # Mock interface to the graph store.
    # Later, mock more actual responses

    def in_era(*args):
        graph = rdflib.Graph()
        dummy = os.path.join(os.path.dirname(__file__),
                             '../data/jurassic_tm.ttl')
        graph.parse(dummy, format='ttl')
        return graph


async def load_test_graph():
    return MockGraph()

app.dependency_overrides[load_graph] = load_test_graph


def test_code():
    code = 'MMG'
    response = client.get(f"/lex/{code}")
    assert response.status_code == 200


def test_era():
    name = 'Carboniferous'
    response = client.get(f"/era/{name}")
    assert response.status_code == 200
    assert 'digraph' in str(response.content)
