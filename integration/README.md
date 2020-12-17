# Integration tests

## Running

Requires a Fuseki container for the SPARQL endpoint:

```
docker-compose -f docker-compose-fuseki.yml up -d
```

This will then populate the DB with sample data (from a query against the main SPARQL endpoint at data.bgs.ac.uk, and with text mined data supplied here in `./data`.

```
export PYTHONPATH=stratigraph
py.test integration
```
