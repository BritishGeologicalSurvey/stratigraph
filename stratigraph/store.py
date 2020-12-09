import os
import rdflib
# import SPARQLWrapper


class GraphStore():
    """Intended as an abstraction in front of a graph store"""

    def in_era(self, name, full=False):
        """
        Returns a stratigraph for a geochronological era.
        This should be the output of a SPARQL CONSTRUCT query
        For now let's return canned data for the Jurassic
        """
        graph = rdflib.Graph()
        # These lines we should replace with a query
        dummy = os.path.join(os.path.dirname(__file__),
                             '../data/jurassic_tm.ttl')
        graph.parse(dummy, format='ttl')
        return graph
