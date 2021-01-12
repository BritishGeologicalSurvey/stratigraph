import os
from functools import reduce
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

    def graph_by_era(self, era_uri, full=False, groups=False):
        """
        Accepts the URI for a geochron concept
        Retrieves the upper/lower boundary relations
        for Lexicon terms with an age range that is contained
        within the geochron concept's age range
        """
        # FILTER clauses not allowed in CONSTRUCT, so append those later to
        # build the WHERE clause
        construct = """
            ?lex lex:hasYoungestAgeValue ?minAge .
            ?lex lex:hasOldestAgeValue ?maxAge .
            ?lex lex:hasRockUnitRank ?rank .
            ?era geochron:minAgeValue ?eraMinAge .
            ?era geochron:maxAgeValue ?eraMaxAge .
            ?lex rdfs:label ?label .
           """
        upper_link = "?lex ext:upper ?upper ."
        lower_link = "?lex ext:lower ?lower ."

        upper_lower_optional = """
            OPTIONAL { ?lex ext:upper ?upper }
            OPTIONAL { ?lex ext:lower ?lower }
            """
        age_contains_filter = """
            FILTER ( xsd:double(?minAge) > xsd:double(?eraMinAge)
                && xsd:double(?maxAge) < xsd:double(?eraMaxAge)
                && ?era = <{0}> 
            )
            """.format(era_uri)

        # age_overlaps_filter provided here but not used yet
        # TODO may want to switch between contains & overlaps?
        age_overlaps_filter = """
            FILTER ((( xsd:double(?eraMaxAge) >  xsd:double(?minAge) 
                     &&  xsd:double(?minAge) >  xsd:double(?eraMinAge) 
                     )
                    || 
                    ( xsd:double(?eraMinAge) <  xsd:double(?maxAge) 
                      ||  xsd:double(?maxAge) < xsd:double(?eraMaxAge))
                    )
                    && ?era = <{0}> 
            )
            """.format(era_uri)  # noqa: F841 E501
        formations_filter = """
            FILTER (?rank= rock:F)
            """
        formations_groups_filter = """
            FILTER (?rank IN (rock:F, rock:G) )
            """

        # CONSTRUCT two graphs, one for upper, one for lower links, add them
        # Because we can't put OPTIONAL fields in a CONSTRUCT clause
        where = construct + upper_lower_optional + age_contains_filter
        graphs = []

        for link in (upper_link, lower_link):
            use_construct = construct + link
            use_where = where
            # unless asking for full graph, only return Formation types
            # TODO if upper or lower not of rank Formation, use skos:broader
            # relations until reach a parent Formation
            # TODO rationalise this once we reach a preferred view
            if not full and not groups:
                use_where += formations_filter
            elif groups:
                use_where += formations_groups_filter

            query = """
                PREFIX lex: <http://data.bgs.ac.uk/ref/Lexicon/>
                PREFIX geochron: <http://data.bgs.ac.uk/ref/Geochronology/>
                PREFIX rock: <http://data.bgs.ac.uk/id/Lexicon/RockUnitRank/>
                PREFIX ext: <http://data.bgs.ac.uk/ref/Lexicon/Extended/>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>
                CONSTRUCT {{
                    {0}
                }}
                WHERE {{
                    {1}
                }}""".format(use_construct, use_where)

            logging.debug(query)

            sparql = SPARQLWrapper(ENDPOINT)
            sparql.setQuery(query)

            graphs.append(self.try_sparql_query(sparql))

        # Nice feature of rdflib to combine graphs with + operator
        def sum_graphs(g1, g2):
            return g1 + g2

        return reduce(sum_graphs, graphs)

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
