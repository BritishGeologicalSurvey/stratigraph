import os
import logging
from urllib.error import URLError, HTTPError

from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound

logging.basicConfig(level=logging.DEBUG)

DB = 'stratigraph'
ENDPOINT = os.environ.get(
    'ENDPOINT',
    f'http://localhost:3030/{DB}/query')


class GraphStore():
    """Intended as an abstraction in front of a graph store"""

    def in_era(self, era_uri, full=False):
        """
        Returns a stratigraph for a geochronological era.
        (in the form of an rdflib.Graph)
        This should be the output of a SPARQL CONSTRUCT query
        """
        return self.graph_by_era(era_uri, full=full)

    def graph_by_era(self, era_uri, full=False):
        """
        Accepts the code for a geochron concept
        Retrieves the upper/lower boundary relations
        for Lexicon terms with an age range that is contained within the geochron cnncept's age range
        Change to 
        # FILTER ((?eraMaxAge > ?minAge && ?minAge > ?eraMinAge) || (?eraMinAge < ?maxAge || ?maxAge < ?eraMaxAge)) # for units overlapping the era
        """

        construct = """
            ?lex lex:hasYoungestAgeValue ?minAge .
            ?lex lex:hasOldestAgeValue ?maxAge .
            ?era a skos:Concept .
            ?era skos:inScheme <http://data.bgs.ac.uk/ref/Geochronology> .
            ?era geochron:minAgeValue ?eraMinAge .
            ?era geochron:maxAgeValue ?eraMaxAge .
            ?subject rdfs:label ?label .
            OPTIONAL { ?subject ext:upper ?upper }
            OPTIONAL { ?subject ext:lower ?lower }
            """
        where = construct+"""
            FILTER ((?minAge > ?eraMinAge) && (?maxAge < ?eraMaxAge))
            FILTER (?era = {0} )
            """.format(era_uri)

        # unless asking for full graph, only return Formation types
        # TODO if upper or lower are not of rank Formation, use skos:broader relations until reach a parent Formation
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
                {1}
            }}""".format(construct,where)

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
