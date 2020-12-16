"""Load Jurassic data from data.bgs.ac.uk, and our sample text mined data,
into an in-memory Fuseki store - useful to run integration tests in CI
(Based on a test done for VocPrez showing this approach to CI)
"""

import logging
import os
from urllib.parse import urljoin
from SPARQLWrapper import SPARQLWrapper
import requests
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.DEBUG)

DBNAME = 'stratigraph'
FUSEKI_HOST = os.environ.get('FUSEKI_HOST', 'http://localhost:3030/')
ENDPOINT = 'http://data.bgs.ac.uk/vocprez/endpoint'

# "Assembler file" to HTTP POST create new dataset in Fuseki
DB = """PREFIX tdb:     <http://jena.hpl.hp.com/2008/tdb#>
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ja:      <http://jena.hpl.hp.com/2005/11/Assembler#>
<#dataset> rdf:type         tdb:DatasetTDB ;
    tdb:location "DB" ;"""

# Query to collect Jurassic data from bgs.ac.uk
CONSTRUCT = """
            ?lex lex:hasYoungestAgeValue ?minAge .
            ?lex lex:hasOldestAgeValue ?maxAge .
            ?era geochron:minAgeValue ?eraMinAge .
            ?era geochron:maxAgeValue ?eraMaxAge .
            ?lex ?predicate ?object .
            """

FILTER = """
            FILTER ((?minAge > ?eraMinAge) && (?maxAge < ?eraMaxAge))
            FILTER (?era = <http://data.bgs.ac.uk/id/Geochronology/Division/J> )
            """

WHERE = CONSTRUCT+FILTER

QUERY = """PREFIX lex: <http://data.bgs.ac.uk/ref/Lexicon/>
           PREFIX geochron: <http://data.bgs.ac.uk/ref/Geochronology/>
           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
           CONSTRUCT {{
                {0}
            }}
            WHERE {{ {1}}}""".format(CONSTRUCT, WHERE)



def create_db(name=DBNAME):
    logging.debug("in create_db")
    response = requests.post(urljoin(FUSEKI_HOST, '$/datasets'),
                             data=DB,
                             auth=HTTPBasicAuth('admin', 'hello'),
                             params={'dbType': 'mem',
                                     'dbName': name})
    logging.debug("create_db")

    response.raise_for_status()


def add_sparql_data():
    """Collect everything where the age is contained within the Jurassic age range
    Should we include anything that overlaps the Jurassic?
    """
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(QUERY)

    logging.debug(QUERY)

    results = sparql.query().convert()

    data = results.serialize(format='nt')

    status = requests.put(
            urljoin(FUSEKI_HOST, f'{DBNAME}/data?default'),
            headers={'Content-type': 'application/n-triples'},
            data=data)
    status.raise_for_status()


def add_local_data():
    """Add in our text mined sample from the Jurassic"""
    with open('./data/jurassic_tm.ttl', 'r') as infile:
        jurassic = infile.read()
        status = requests.post(
                urljoin(FUSEKI_HOST, f'{DBNAME}/data?default'),
                headers={'Content-type': 'text/turtle'},
                data=jurassic)
        status.raise_for_status()


if __name__ == '__main__':
    try:
        create_db()
    except Exception as err:
        print(err)
    add_sparql_data()
    add_local_data()
