"""
API to provide SVG, TTL, DOT export from a graph store.
Currently uses Fuseki as a backend for SPARQL queries
"""

# If we end up with POST queries, we'll want these
# to constrain and verify input with
# from typing import List
# from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException
from stratigraph.graph import Graph


def load_graph():
    """Interface to our graph store.
    Loaded via Depends() below to make mock testing much easier
    """
    try:
        # load up a graph model here
        graph = Graph()
    except Exception:  # handle explicit exceptions - no endpoint, etc
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph


app = FastAPI()


@app.get("/lex/{code}")
async def lex_code(code: str, graph=Depends(load_graph)):
    """
    Given a Lexicon code, return a nearby graph.
    Optional distance from the Lexicon term, plus default?
    Optional response format (SVG, ttl, dot etc)? - default?
    """
    return {}


@app.get("/era/{name}")
async def geo_era(name: str, graph=Depends(load_graph)):
    """
    Given a Geochron term, return the graph filtered by everything
    that fits inside this geochronological era
    """
    return {}
