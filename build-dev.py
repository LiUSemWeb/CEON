#!/usr/bin/env python3
from glob import glob
import os
from rdflib import Graph
import re

def copy_ontologies():
    """Copy dev ontologies to web path."""

    for source in glob("ontology/modules/*/*/*", recursive=True):
        if not source.endswith(".ttl"):
            continue
        #output = f"docs/ontology/{filename.split('ontology/modules/')[1]}"
        #print("from:", filename)
        #print("to:", output)
        parts = re.match("ontology/modules/([^/]*)/([^/]*)", source)    
        name = parts.group(1)
        version = parts.group(2)
        base = f"docs/ontology/{name}/{version}/{name}"
        
        os.makedirs(f"docs/ontology/{name}/{version}/", exist_ok=True)
        g = Graph()
        g.parse(source)
        g.serialize(destination=f"{base}.ttl", format="turtle")
        g.serialize(destination=f"{base}.rdf", format="xml")
        g.serialize(destination=f"{base}.owl", format="xml")
        g.serialize(destination=f"{base}.jsonld", format="json-ld")


if __name__ == "__main__":
    copy_ontologies()
