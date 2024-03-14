#!/usr/bin/env python3
from glob import glob
import os
from rdflib import Graph
import re
import logging

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)

def copy_ontologies():
    """Copy ontologies to web path."""
    map = {
        "modules": "ontology",
        "demo": "demo"
    }

    for type in ["modules", "demo"]:
        # publish ontologies
        for source in sorted(glob(f"ontology/{type}/*/*/*", recursive=True)):
            if not source.endswith(".ttl"):
                continue
            
            parts = re.match(f"ontology/{type}/([^/]*)/([^/]*)", source)    
            name = parts.group(1)
            version = float(parts.group(2))
            target = f"docs/{map[type]}/{name}/{version}/"
            os.makedirs(target, exist_ok=True)
            
            logging.debug(f"Source:\t{source}")
            logging.debug(f"Name:\t{name}")
            logging.debug(f"Target:\t{target}")
            
            g = Graph()
            g.parse(source)
            g.serialize(destination=f"{target}{name}.ttl", format="turtle")
            g.serialize(destination=f"{target}{name}.rdf", format="xml")
            g.serialize(destination=f"{target}{name}.owl", format="xml")
            g.serialize(destination=f"{target}{name}.jsonld", format="json-ld")


if __name__ == "__main__":
    copy_ontologies()
