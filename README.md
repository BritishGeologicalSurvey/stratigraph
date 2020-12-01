# Network Stratigraphy through text mining

## Licence

Text and data is made available through the UK Open Government Licence.
Associated code is available through the LGPL v3 open source licence.

## Processing steps

### Generating graph data from sources


1. Extract lower boundary description, upper boundary description and label from lexicon linked data (where rank is formation*) using vocprez sparql endpoint (public endpoint). *members and beds of interest later but don't have stratigraphic relationship to formation, it's a different sort of relationship, so ignore for now.

2. Run NER stratigraph tool on those descriptions to identify formations in Lexicon upper boundary and lower boundary descriptions

3. Run similarity matching to resolve formations to concepts in the lexicon linked data

4. Remove matches where self is matched

5. If rank of the matched unit is not a formation, query linked data using sparql endpoint to generalise units to their parent formation

6. Capture the relationship between a lexicon unit and the matched lexicon unit, and serialise as ttl

7. Convert ttl to .dot and csv (controversial!)

8. Load into fuseki store

9. BONUS FEATURE: Convert to Loop GSO (good for long term interoperability, dependent on finalisation of GSO)

10. Push to github (for version control, providing downloads)

### API

TODO - define the endpoints on the graph database that the visualisation needs to use


### Visualisation
   

Import dot file into visualisation, allowing multiple imports
	(BONUS FEATURE: allow import of ttl using Loop GSO schema - or call service that can convert from Loop GSO to dot)

Toggle to hide member/bed and only view generalisation at formation level

Display source of data alongside the graph, highlight the matched term in the free text (similar to the text mining work). 

?Feedback mechanism for individual matches from free text

Editing of aggregated graph data, save to new graph, include provenance of nodes and edges

?Save graph as dot, csv, ttl, ttl using Loop GSO


## Contributors

* Tim Kearsey
* Jo Walsh
* Rehan Kaleem
* Rachel Heaven
