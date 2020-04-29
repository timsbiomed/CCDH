# CCDH
Code specific to the CCDH Terminology Work

## Extracting value sets from caDSR

Working with the [CRDC Data Model Dictionaries](https://docs.google.com/spreadsheets/d/1QhipywHWStrNz1Pm8o6fmsXixLcfmb8aWfy6ww9NA4Y/edit?pli=1#gid=1749412622).

Given:
1) A caDSR Data Element Public Id (e.g. [5432594](https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432594&version=1.0))
2) The current RDF version of the caDSR (at the moment, the RDF version is not public -- I contact Gilberto Fragosio to get an image)
3) The current RDF version of the NCI Thesaurus (OWL version is public, modified version used here is not)
4) A reaonably current RDF version of the UMLS -- this can be found on the BioPortal SPARQL Endpoint (location TBD)

In circumstances where the permissible values are available, the [following query](http://graph.hotecosystem.org:7200/sparql?name=PVtoNCIt3&infer=true&sameAs=true&query=PREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX+cmdr%3A+%3Chttp%3A%2F%2Fcbiit.nci.nih.gov%2FcaDSR%23%3E%0APREFIX+isomdr%3A+%3Chttp%3A%2F%2Fwww.iso.org%2F11179%2FMDR%23%3E%0APREFIX+ncit%3A+%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23%3E%0Aselect+DISTINCT+%3Fvalue+%3Fncit_concept+%3Fconcept_name+%3Frole+%3Forder+where+%7B%0A++++%3Fs+cmdr%3ApublicId+%223111302%22+.%0A++++%3Fs+isomdr%3Apermitted_value+%3Fpv+.%0A++++%3Fpv+isomdr%3Avalue+%3Fvalue+.%0A++++%3Fpv+cmdr%3Ahas_concept+%3Fcd+.%0A++++%3Fcd+%3Frole+%3Fncit_concept+.%0A++++%3Fcd+cmdr%3Adisplay_order+%3Forder+.%0A++++%3Fncit_concept+rdfs%3Alabel+%3Fconcept_name+.%0A%7D%0A):

```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cmdr: <http://cbiit.nci.nih.gov/caDSR#>
PREFIX isomdr: <http://www.iso.org/11179/MDR#>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
select DISTINCT ?value ?ncit_concept ?concept_name ?role ?order where {
    ?s cmdr:publicId "3111302" .
    ?s isomdr:permitted_value ?pv .
    ?pv rdfs:label ?value .
    ?pv cmdr:has_concept ?cd .
    ?cd ?role ?ncit_concept .
    ?cd cmdr:display_order ?order .
    ?ncit_concept rdfs:label ?concept_name .
}
```
produces

| value | ncit_concept | concept_name | role | order |
| --- | --- | --- | --- | --- |
| Bone Marrow | UNK:C12431 | Bone Marrow | cmdr:main_concept | 0 |
| Saliva | UNK:C13275 | Saliva | cmdr:main_concept | 0 |
| ... |
| Mononuclear Cells from Bone Marrow | UNK:C12431 | Bone Marrow | cmdr:main_concept | 0 |
| Mononuclear Cells from Bone Marrow | UNK:C42885 | Derivation | cmdr:minor_concept | 1 |
| Mononuclear Cells from Bone Marrow | UNK:C73123 | Mononucleated Blood Cell | cmdr:minor_concept | 2 |

Notes:
1) The 'UNK' URI prefix is actually http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl# -- the "." in the
path causes a lot of the RDF tools heartburn.
2) The "Mononuclear Cells from Bon Marrow" caDSR entry uses "coordination by juxtaposition" -- this is going to present
an interesting challenge when it comes to mapping.

The above output can be used to produce text value set (We need to discuss how tables of permissible values can be 
mapped to codes)

Assuming that the coordination issues can be addressed, the NCIt Concepts provide a jumping-off point to:
1) The NCI Thesaurus.  The [query](http://graph.hotecosystem.org:7200/sparql?name=PVtoNCIt&infer=true&sameAs=true&query=select+distinct+*+WHERE+%7B%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23C812%3E+%3Fp+%3Fo%7D%0A):
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select distinct ?l ?o WHERE {
    <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12431> ?p ?o.
	?p rdfs:label ?l .
}
```

Gives us everything that we know about the particular NCIt concept including the value sets (NCI Subsets)
it is a member of and its mappings to other code systems -- a key one of which is the UMLS CUI. (e.g. C0005953)

The UMLS CUI, in turn, gives us an entry point into the UMLS, an RDF representation of which is available
in BioPortal -- this gives us a bridge into everything that "maps to" the UMLS concept.