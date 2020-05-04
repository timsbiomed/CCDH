from rdflib import RDF
from sparql_slurper import SlurpyGraph


g = SlurpyGraph("http://graph.hotecosystem.org:7200/repositories/crfcde")
g.persistent_bnodes = True
g.limit = 100
for t in g.subject_objects(RDF.type):
    print(t)