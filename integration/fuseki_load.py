"""Load Jurassic data from data.bgs.ac.uk, and our sample text mined data,
into an in-memory Fuseki store - useful to run integration tests in CI
(Based on a test done for VocPrez showing this approach to CI)
"""

import os
from urllib.parse import urljoin
from SPARQLWrapper import SPARQLWrapper
import requests
from requests.auth import HTTPBasicAuth

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
 ?subject lex:hasBroaderPredominantAge "Jurassic"@en .
 ?subject ?predicate ?object .
"""

QUERY = """PREFIX lex: <http://data.bgs.ac.uk/ref/Lexicon/>
           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
           CONSTRUCT {{
                {0}
            }}
            WHERE {{ {0} }}""".format(CONSTRUCT)


def create_db(name=DBNAME):
    response = requests.post(urljoin(FUSEKI_HOST, '$/datasets'),
                             data=DB,
                             auth=HTTPBasicAuth('admin', 'admin'),
                             params={'dbType': 'mem',
                                     'dbName': name})

    response.raise_for_status()


def add_sparql_data():
    """Collect everything that hasBroaderPredominantAge "Jurassic"@en
    Will we miss data this way?
    """
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(QUERY)
    results = sparql.query().convert()

#    headers = {'Accept': 'application/n-triples'}

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
        status = requests.put(
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
