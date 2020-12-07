from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from stratigraph.api import app, load_graph

client = TestClient(app)


class MockGraph(MagicMock):
    pass

# Later, mock some actual responses
#    def from_code(*args):
#        return rdflib.Graph()


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
