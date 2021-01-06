"""Collect RDF namespaces.
Look at how we could improve this with namespace_manager;
But it requires an rdflib.Graph which we don't always have.
https://rdflib.readthedocs.io/en/stable/namespaces_and_bindings.html"""  # noqa: E501

from rdflib import Namespace

GEOCHRON = Namespace('http://data.bgs.ac.uk/id/Geochronology/Division/')
LEXICON = Namespace('http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/')
LEX_EXT = Namespace('http://data.bgs.ac.uk/ref/Lexicon/Extended/')
