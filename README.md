# Network Stratigraphy through text mining

## Install and run tests

```
pip install -r requirements.txt
export PYTHONPATH=.
py.test tests
```

There are also a set of integration tests that depend on

* Stanford CoreNLP Server with the [BGS custom model for Lexicon and Geochronology named entity recognition](https://github.com/BritishGeologicalSurvey). See the instructions in that project for [Running CoreNLP in docker](https://github.com/BritishGeologicalSurvey/geo-ner-model#running-in-docker) using our docker image in Github Container Registry.

* An RDF graph store with a [SPARQL endpoint](https://medium.com/virtuoso-blog/what-is-a-sparql-endpoint-and-why-is-it-important-b3c9e6a20a8b). We provide configuration for doing this with [Apache Jena Fuseki](https://github.com/stain/jena-docker/) running in docker.

You can see these tests run in a [Github Actions workflow](https://github.com/BritishGeologicalSurvey/stratigraph/blob/main/.github/workflows/integration.yml) with Fuseki and CoreNLP Server running as docker services.

## Running the application

This will run two docker containers, the stratigraph API service and the Fuseki RDF triplestore:

```
docker-compose up -d
```

On first run this will build the API container (which you can also build with `docker build . -t bgs/strat`. Fuseki (the graph store) will look in `./data/fuseki` for its databases and the Fuseki container will create this directory if it doesn't exist.

### Load with testing data

At present the easiest way to get running with sample data is to use the same script as the integration tests (which collects a subset of [BGS Lexicon of Named Rock Units](https://data.bgs.ac.uk/doc/Lexicon.html) and [Geochronolog](https://data.bgs.ac.uk/doc/Geochronology.html) data from the SPARQL endpoint at [data.bgs.ac.uk](https://data.bgs.ac.uk/) and then loads the sample extract of the Jurassic graph included in this repository. (Requires Python 3). This creates the `stratigraph` database if not already present.

With Fuseki running locally in docker:

```
export PYTHONPATH=.
pip install -r requirements.txt
python integration/fuseki_load.py
```

The ideal is to improve the distribution so that Fuseki loads the whole Lexicon graph on startup, with the ability to reproduce the dataset from scratch using the[custom CoreNLP server container](https://github.com/BritishGeologicalSurvey/geo-ner-model#running-in-docker) as above.

### Load with full BGS Stratigraphy data

For the full application, the triplestore should contain the full dataset for the BGS Lexicon and Geochronology Linked Open Data. Both [vocabularies can be downloaded in n-triples format](https://github.com/BritishGeologicalSurvey/vocabularies/tree/main/vocabularies); data are made available under the [UK Open Government Licence](https://www.bgs.ac.uk/bgs-intellectual-property-rights/open-government-licence/).

With [custom Stanford CoreNLP server](https://github.com/BritishGeologicalSurvey/geo-ner-model#running-in-docker) running in docker:

```
python scripts/all_triples.py
```

This will go through the following steps:

* Collect all BGS Lexicon entries for rock units that have text descriptions of their supper/lower boundary relations
* Extract Lexicon names from those text descriptions and link them, where possible, to Linked Data URLs.
* Create a graph of upper/lower boundary links between rock units inferred from the text, and write it as a single file in Turtle format at `./data/all_lexicon.ttl`

The Stratigraph application requires this file, and the n-triples for the whole of the BGS Lexicon and Geochronology, imported into the Fuseki triplestore. (See `integration/fuseki_load.py` for methods for doing this programmatically, or import the dataset using Fuseki's admin UI)

## Licence

Text and data is made available through the UK Open Government Licence.
Associated code is available through the LGPL v3 open source licence.

## Contributors

* Tim Kearsey
* Jo Walsh
* Rehan Kaleem
* Rachel Heaven
* Vyron Christodoulou
