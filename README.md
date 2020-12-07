# Network Stratigraphy through text mining

## Install and run tests

```
pip install -r requirements.txt
export PYTHONPATH=.
py.test
```

## Running

The scripts and tests depend on having Stanford CoreNLP Server with the BGS custom model for Lexicon and Geochronology named entity recognition.

See the instructions in that project for [Running CoreNLP in docker](https://github.com/BritishGeologicalSurvey/geo-ner-model#running-in-docker) using our docker image in Github Container Registry. This requires authentication; see also (https://docs.github.com/en/free-pro-team@latest/packages/getting-started-with-github-container-registry/migrating-to-github-container-registry-for-docker-images#authenticating-with-the-container-registry)[authenticating with the Github Container Registry]

Note - eventually we want a multi-container network with (graph storage/query), (text mining service) and (application API and frontend)


## Licence

Text and data is made available through the UK Open Government Licence.
Associated code is available through the LGPL v3 open source licence.

## Contributors

* Tim Kearsey
* Jo Walsh
* Rehan Kaleem
* Rachel Heaven
* Vyron Christodoulou
