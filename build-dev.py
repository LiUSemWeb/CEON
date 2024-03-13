#!/usr/bin/env python3
from glob import glob
import os
from rdflib import Graph
import re

def copy_ontologies():
    """Copy dev ontologies to web path."""
    map = {
        "modules": "ontology",
        "demo": "demo"
    }
    
    for type in ["modules", "demo"]:
        for source in glob(f"ontology/{type}/*/*/*", recursive=True):
            if not source.endswith(".ttl"):
                continue

            parts = re.match(f"ontology/{type}/([^/]*)/([^/]*)", source)    
            name = parts.group(1)
            version = parts.group(2)
            base = f"docs/{map[type]}/{name}/{version}/{name}"
            os.makedirs(f"docs/{map[type]}/{name}/{version}/", exist_ok=True)
            g = Graph()
            g.parse(source)
            g.serialize(destination=f"{base}.ttl", format="turtle")
            g.serialize(destination=f"{base}.rdf", format="xml")
            g.serialize(destination=f"{base}.owl", format="xml")
            g.serialize(destination=f"{base}.jsonld", format="json-ld")


if __name__ == "__main__":
    copy_ontologies()
