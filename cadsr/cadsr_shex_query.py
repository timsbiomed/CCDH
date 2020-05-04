import os
from typing import Dict

from pyshex import ShExEvaluator
from rdflib import Literal, Namespace
from sparql_slurper import SlurpyGraph, GraphDBSlurpyGraph

CMDR = Namespace('http://cbiit.nci.nih.gov/caDSR#')

# The query should really take the literal for the public id and reverse it to get the ata element.  For the moment,
# we do the first step manually
g = GraphDBSlurpyGraph("http://graph.hotecosystem.org:7200/repositories/crfcde")

focus = list(g.subjects(CMDR.publicId,  Literal("3111302")))[0]
cwd = os.path.dirname(__file__)
shex_path = os.path.join(cwd, 'shex')
shex_file = os.path.join(shex_path, 'cadsr_valueset.shex')
rdf_path = os.path.join(cwd, 'json')
formats: Dict[str, str] = {'turtle': 'ttl', 'json-ld': 'json', 'ntriples': 'nt'}


# results = ShExEvaluator(g, shex_file, Literal("5432508")).evaluate(debug=False)
results = ShExEvaluator(g, shex_file, focus,over_slurp=False).evaluate(debug=False)
success = all(r.result for r in results)
if not success:
    for r in results:
        if not r.result:
            print(r.reason)
else:
    for fmt, suffix in formats.items():
        fn = os.path.join(rdf_path, 'cadsr_valueset.' + suffix)
        g.serialize(fn, format=fmt)
        print(f"{fn} written")
