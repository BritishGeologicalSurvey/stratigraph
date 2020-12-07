# Source data and processed samples

## Data extracted through text mining

Run `scripts/jurassic_triples.py` to produce:

 * [Turtle format upper/lower boundary relations in Jurassic](jurassic_tm.ttl)

Requires our custom build of CoreNLP Server running locally. To pull down the docker image from docker package repository on first use you need to create a personal access token in your github account (https://github.com/settings/tokens) with read:packages permissions

Save the token in a text file e.g. TOKEN.txt and then pass this into the docker login command before pulling the docker image. NB this always gives a login succeed message even if the token is wrong.

```
cat TOKEN.txt | docker login https://docker.pkg.github.com -u username --password-stdin

docker pull docker.pkg.github.com/britishgeologicalsurvey/geo-ner-model/corenlp:v0.3

docker run -p 9000:9000 docker.pkg.github.com/britishgeologicalsurvey/geo-ner-model/corenlp:v0.3
```

## Graphviz visualisation

Run `scripts/ttl_to_dot.py` to produce:

 * [Graphviz dotfile format upper/lower boundary relations in Jurassic frm ttl file](jurassic_tm.dot)

 
Install and use graphviz `dot` utility using following commands

```
pip install graphviz

sudo apt-get install graphviz  [had to do this on Ubuntu 18.04.1 LTS]

dot -Tsvg data/jurassic_tm.dot -o data/jurassic_tm.svg
```

 to produce:
 
 * [SVG output from dotfile](jurassic_tm.svg)