#!/usr/bin/env python3
import os
import yaml

def copy_ontologies(config):
    """Copy ontologies to web path."""
    for ontology in config["ontologies"]:
        source = ontology["source"]
        dirname = ontology["path"]
        version = ontology["version"]
        os.system(f"mkdir -p docs/ontology-network/{dirname}/{version}")
        os.system(f"cp {source} docs/ontology-network/{dirname}/{version}/")


def main():
    with open("config.yml", 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    copy_ontologies(config)


if __name__ == "__main__":
    main()