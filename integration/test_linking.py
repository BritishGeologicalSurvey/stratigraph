"""
Test the effect of extending stopwords list
on programmatic linking of NER to Linked Data URLs
"""
import stratigraph.similar
import json

def test_extend_list():
    extend_with = ['Member', 'Bed', 'Beds']
    # Bad form to amend a constant, but testing
    # print(STOP_WORDS)
    stratigraph.similar.STOP_WORDS += extend_with

    similar = stratigraph.similar.Similar()
    missing = './data/sort_missing_names.json'
    found = []
    with open(missing) as name_list:
        missed_names = json.load(name_list)
        for name in missed_names:
            closest = similar.most_similar(name)
            if closest:
                found.append(closest)
        with open('./data/found_names.json', 'w') as out:
            out.write(json.dumps(found, indent=2))
