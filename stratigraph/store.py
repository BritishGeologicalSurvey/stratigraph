import os
import logging
from urllib.error import URLError, HTTPError

import rdflib
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound

logging.basicConfig(level=logging.INFO)

DB = 'stratigraph'
ENDPOINT = os.environ.get(
    'ENDPOINT',
    f'http://localhost:3030/{DB}/query')


class GraphStore():
    """Intended as an abstraction in front of a graph store"""

    def in_era(self, name, full=False):
        """
        Returns a stratigraph for a geochronological era.
        (in the form of an rdflib.Graph)
        This should be the output of a SPARQL CONSTRUCT query
        """
        return self.graph_by_era(name, full=full)

    def graph_by_era(self, name, full=False):
        """
        Accepts a BGS Linked Data URL
        Retrieves the upper/lower boundary relations
        for Lexicon terms with 'hasBroaderPredominantAge'
        that matches this URL
        TODO - using `name` until we change to URL
        """

        where = """
            ?subject lex:hasBroaderPredominantAge "{0}"@en .
            ?subject ext:upper ?upper .
            ?subject ext:lower ?lower .
            ?subject rdfs:label ?label .""".format(name)

        # unless asking for full graph, only return Formation types
        if not full:
            where += "\n ?subject lex:hasRockUnitRank rock:F ."

        query = """
            PREFIX lex: <http://data.bgs.ac.uk/ref/Lexicon/>
            PREFIX rock: <http://data.bgs.ac.uk/id/Lexicon/RockUnitRank/>
            PREFIX ext: <http://data.bgs.ac.uk/ref/Lexicon/Extended/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            CONSTRUCT {{
                {0}
            }}
            WHERE {{
                {0}
            }}""".format(where)

        logging.debug(query)

        sparql = SPARQLWrapper(ENDPOINT)
        sparql.setQuery(query)
        return self.try_sparql_query(sparql)

    def try_sparql_query(self, sparql):
        """Get results from a sparql query, handling some error states.
        Returns an rdflib.Graph() which may be empty"""
        results = None
        try:
            results = sparql.query().convert()
        except (HTTPError, QueryBadFormed) as err:
            logging.error({'msg': str(err)})
        except (URLError, EndPointNotFound) as err:
            logging.error({'state': 'Could not reach sparql server',
                           'msg': str(err)})
        finally:
            if not results:
                results = Graph()
        logging.debug(results)
        return results
