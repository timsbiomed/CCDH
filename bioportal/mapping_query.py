from rdflib import RDF
from sparql_slurper import SlurpyGraph, QueryResultPrinter

g = SlurpyGraph("http://sparql.bioontology.org")
g.limit = 100
g.add_result_hook(QueryResultPrinter)

for t in g.subject_objects(RDF.type):
    print(t)