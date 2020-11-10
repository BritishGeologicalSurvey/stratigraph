import re
import logging

from Levenshtein import distance
from SPARQLWrapper import SPARQLWrapper, JSON

STOP_WORDS = [
    "Formation",
    "Formations",
    "Group",
    "Groups",
    "Supergroup",
    "Period",
    "Periods",
    "Sub-age",
    "Sub-ages",
    "Age",
    "Ages",
    "Sub-epoch",
    "Sub-epochs",
    "Era",
    "Eras",
    "Eon",
    "Eons",
    "Epoch",
    "Epochs",
    "Sub-period",
    "Sub-periods",
    "Sub-era",
    "Sub-eras",
    "Sub-eon",
    "Sub-eons"]

EDIT_DIST_CUT = 0.89  # cutoff for Levenshtein similarity set by @ike

# Slow
# LEXICON_TRIPLES = "https://raw.githubusercontent.com/BritishGeologicalSurvey/vocabularies/main/vocabularies/lexicon-named-rock-unit.nt"  # noqa: E501

ENDPOINT = "https://data.bgs.ac.uk/vocprez/endpoint"

SPARQL_QUERY = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?url ?name
WHERE { ?url rdfs:label ?name . }
"""


def remove_stop_words(term):
    """Do fuzzy string matching after removing stopwords listed above"""
    for word in STOP_WORDS:
        term = re.sub(r"\b%s\b" % word, "", term)
        term = term.rstrip()
    return term


def stopped_word(term):
    """Show stopword removed a term (returns only the stopword)"""
    stopped = None
    for word in STOP_WORDS:
        stop_search = re.compile(r"\b%s\b" % word, re.I)
        match = stop_search.search(term)
        if match:
            stopped = match[0]
    return stopped


def concept_index():
    """Create a name -> link mapping with a SPARQL query.
    We run this against the SPARQL endpoint at data.bgs.ac.uk
    (Could within rdflib reading a graph from a file, is slow)
    """
    name_index = []
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(SPARQL_QUERY)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        name_index.append([result["name"]["value"], result["url"]["value"]])

    return name_index


class Similar:

    def __init__(self):
        self.match_links = self.get_links()

    def get_links(self):
        """Build a list of names, stopwords removed and originals,
        plus Linked Data URLs, to match incoming names against"""
        match_links = []
        for row in concept_index():
            short = remove_stop_words(row[0])
            row = [short] + row
            match_links.append(row)
        return match_links

    @staticmethod
    def normalised_similarity(term1, term2):
        """Returns normalised levenshtein similarity between terms
        Uses the workings here:
        info.debatty.java.stringsimilarity.NormalizedLevenshtein"""
        ## TODO some terms come back as None.
        ## Are URLs missing rdfs labels, or NER extracted all stopwords?
        ## Needs investigation
        if not term1 or not term2:
            return 0
        return 1.0 - distance(term1, term2) / max(len(term1), len(term2))

    def most_similar(self, term, cut=EDIT_DIST_CUT):
        """Finds the most similar term by normalised Levenshtein distance,
        filtered by a cutoff value of 0.89.
        Returns either None, or an entry from the BGS Lexicon

        Now checks that stopwords don't clash - e.g. Oolite Formation
        won't return Oolite Group. So we can add Group(s)/Supergroup(s)
        """
        logging.debug(term)
        name = remove_stop_words(term)

        top_score = 0
        top_match = None
        for word in self.match_links:
            distance = self.normalised_similarity(name, word[0])
            if distance != 0 and distance >= cut and distance > top_score:
                top_match = word
                top_score = distance

        if top_match and name != term:
            name_stop = stopped_word(term)
            matched_stop = stopped_word(top_match[1])
            # Don't return 'Formation' if handed 'Group'
            if name_stop != matched_stop:
                top_match = None

        return top_match


if __name__ == '__main__':
    s = Similar()
    s.most_similar('Patrick Burn Formation')
