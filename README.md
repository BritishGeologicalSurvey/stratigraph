# Network Stratigraphy through text mining

## Install and run tests

```
pip install -r requirements.txt
export PYTHONPATH=.
py.test
```

## Running the text mining

The scripts and tests depend on having Stanford CoreNLP Server with the BGS custom model for Lexicon and Geochronology named entity recognition.

See the instructions in that project for [Running CoreNLP in docker](https://github.com/BritishGeologicalSurvey/geo-ner-model#running-in-docker) using our docker image in Github Container Registry. As of writing, this requires authentication with a personal access token associated with a Github account; please see [authenticating with the Github Container Registry](https://docs.github.com/en/free-pro-team@latest/packages/getting-started-with-github-container-registry/migrating-to-github-container-registry-for-docker-images#authenticating-with-the-container-registry) for detail. The summary is as follows:

* [Create a Personal Access Token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) with rights to `read:packages`; once logged in, start at [Developer Settings/Tokens](https://github.com/settings/tokens)

747c1e0ae5e50472e318934398b88d68a8b12ae0
* Use the personal access token to `docker login` before pulling down the image:
```
 export CR_PAT=YOUR_TOKEN
 echo $CR_PAT | docker login docker.pkg.github.com -u USERNAME --password-stdin
 ...
 docker pull docker.pkg.github.com/britishgeologicalsurvey/geo-ner-model/corenlp:v0.3
```

## Running the application

Kill any existing containers using port 80 or 3030

```
docker container ls
docker rm -f <container-name>
```

```
docker-compose up -d
```

On first run this should build the API container (which you can also build with `docker build . -t bgs/strat`.
Fuseki (the graph store) will look in `./data/fuseki` for its databases and the Fuseki container will create this directory if it doesn't exist.

At present the easiest way to get running with sample data is to use the same script as the integration tests (which collects some BGS Lexicon data from [data.bgs.ac.uk](https://data.bgs.ac.uk/) and then loads the sample extract of the Jurassic graph included in this repository. (Requires Python 3).


```
export PYTHONPATH=.
pip install -r requirements.txt
python integration/fuseki_load.py
```

The intention is to improve the distribution so that Fuseki loads the whole Lexicon graph on startup, with the ability to reproduce the dataset from scratch using the [custom CoreNLP server container](https://github.com/BritishGeologicalSurvey/geo-ner-model#running-in-docker) as above.


## Licence

Text and data is made available through the UK Open Government Licence.
Associated code is available through the LGPL v3 open source licence.

## Contributors

* Tim Kearsey
* Jo Walsh
* Rehan Kaleem
* Rachel Heaven
* Vyron Christodoulou
