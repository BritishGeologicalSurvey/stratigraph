# Source data and processed samples

## Data extracted through text mining

Run `scripts/jurassic_triples.py` to produce:

 * [Turtle format upper/lower boundary relations in Jurassic](jurassic_tm.ttl)
 * [Graphviz dotfile format upper/lower boundary relations in Jurassic](jurassic_tm.dot)

Requires our custom build of CoreNLP Server running locally:

```
docker run -p 9000:9000 docker.pkg.github.com/britishgeologicalsurvey/geo-ner-model/corenlp:v0.3
```
 * [SVG output from dotfile](jurassic_tm.svg)

Produced with this incantation of graphviz `dot` utility

```
dot -Tsvg data/jurassic_tm.dot -o jurassic_tm.svg
```

