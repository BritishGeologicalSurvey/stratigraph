"""
API to provide SVG, TTL, DOT export from a graph store.
Currently uses Fuseki as a backend for SPARQL queries
"""

from typing import Optional
import logging

# If we end up with POST queries, we'll want pydantic
# to constrain and verify input with
# from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from stratigraph.store import GraphStore
from stratigraph.graph import graph_to_dot
from stratigraph.ns import GEOCHRON, LEXICON

logging.basicConfig(level=logging.INFO)


def load_graph():
    """Interface to our graph store.
    Loaded via Depends() below to make mock testing much easier
    """
    try:
        # load up a graph model here
        graph = GraphStore()
    except Exception:  # handle explicit exceptions - no endpoint, etc
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph


app = FastAPI()


@app.get("/lex/{code}")
async def lex_code(code: str,
                   distance: Optional[int] = None,
                   format: Optional[str] = 'dot',
                   colours: Optional[str] = 'digmap',
                   graph=Depends(load_graph)):
    """
    Given a Lexicon code, return a nearby graph.
    Optional distance from the Lexicon term, plus default?
    Optional response format (SVG, ttl, dot etc)? - default?
    """
    uri = str(LEXICON[code])
    print(distance)
    g = graph.graph_from_code(uri, distance=distance)

    if not format or format == 'dot':
        response = graph_to_dot(g, colour_scale=colours)
    if format == 'ttl':
        response = g.serialize(format='ttl')

    return PlainTextResponse(response)


@app.get("/era/{code}")
async def geo_era(code: str,
                  full: bool = False,
                  groups: bool = False,
                  format: Optional[str] = 'dot',
                  colours: Optional[str] = 'digmap',
                  graph=Depends(load_graph)):
    """
    Given a Geochron term, return the graph filtered by everything
    that fits inside this geochronological era

    Optional 'full' to show all units, defaults
    to only show Formation unit rank.

    Optional 'groups' to show both Formation and Group rank

    Optional 'colours' (default 'digmap', or 'age' for ICS colours)
    """
    uri = str(GEOCHRON[code])
    g = graph.graph_by_era(uri, full=full, groups=groups)

    logging.debug(g)
    if not format or format == 'dot':
        response = graph_to_dot(g, colour_scale=colours)
    if format == 'ttl':
        response = g.serialize(format='ttl')

    return PlainTextResponse(response)
    response = ''
