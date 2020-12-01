"""
Talk to the Stanford CoreNLP Server API to extract entities
API documentation: https://stanfordnlp.github.io/CoreNLP/corenlp-server.html
"""
import os
import json
import logging

import requests
from requests.exceptions import ConnectionError

# CoreNLP server address, default
SERVER = os.environ.get(
    'CORENLP_API',
    'http://localhost:9000/')

# Responses we ask for by default (NER in JSON format)
RESPONSE = {"annotators": "tokenize,ssplit,ner", "outputFormat": "json"}


def tokens(document, server=SERVER):
    """Accepts a plain text document, sends the results to a Stanford server.
    Returns the raw JSON output."""
    logging.debug(SERVER)
    request_url = "{}?properties={}".format(SERVER, json.dumps(RESPONSE))
    result = {}
    try:
        response = requests.post(request_url, data=document.encode('utf-8'))
        response.raise_for_status()
        result = response.json()

    except ConnectionError as e:
        logging.debug(e)
        logging.info("Trouble posting to %s", request_url)
        raise

    return result


def entities(document, server=SERVER):
    """Accepts a document, returns a simplified JSON-like list
    of all entities with offsets"""
    try:
        nlp_tokens = tokens(document, server=server)
    except BaseException:
        raise

    entities = []
    for sentence in nlp_tokens.get('sentences', []):
        entities = entities + normalised_entities(sentence['tokens'])
    return entities


def normalised_entities(tokens):
    """Accepts a list of tokens (JSON-like objects returned from Stanford server.
    Returns only the named entities with their offsets.
    Multi-word entities are compressed using the same logic as corenlp-brat.js
    in the interface to the Stanford server.
    Note that the CRFClassifier interface
    does this automatically, but the server doesn't expose that output :/"""
    # https://github.com/stanfordnlp/CoreNLP/blob/master/src/edu/stanford/nlp/pipeline/demo/corenlp-brat.js#L509

    entities = []
    sentence = ''.join([t['originalText'] + t['after'] for t in tokens])

    # The ugly while / +1 syntax here rather than enumerate() is so we can
    # skip ahead in the index
    index = 0
    while index < len(tokens):
        token = tokens[index]
        ner_type = token['ner']
        if ner_type == 'O':
            index = index + 1
            continue

        end_index = index
        while end_index < len(tokens) - \
                1 and tokens[end_index + 1]['ner'] == ner_type:
            end_index += 1
        texts = [t['originalText'] for t in tokens[index:end_index + 1]]
        name = ' '.join(texts)
        entities.append({'name': name,
                         'type': ner_type,
                         'start_char': token['characterOffsetBegin'],
                         'end_char': tokens[end_index]['characterOffsetEnd'],
                         'sentence': sentence})
        index = end_index + 1

    return entities
