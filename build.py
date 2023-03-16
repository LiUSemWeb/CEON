#!/usr/bin/env python3
import os
import yaml
import urllib.request
import zipfile

def copy_ontologies(config):
    """Copy ontologies to web path."""
    for ontology in config["ontologies"]:
        source = ontology["source"]
        dirname = ontology["path"]
        version = ontology["version"]
        os.system(f"mkdir -p docs/ontology-network/{dirname}/{version}")
        os.system(f"cp {source} docs/ontology-network/{dirname}/{version}/")


def download_owl2vowl():
    """Download and extract OWL2VOWL."""
    os.system("mkdir -p temp")
    path_to_jar = "temp/owl2vowl.jar"
    if not os.path.isfile(path_to_jar):
        path_to_zip = "temp/owl2vowl_0.3.7.zip"
        if not os.path.isfile(path_to_zip):
            url = "http://vowl.visualdataweb.org/downloads/owl2vowl_0.3.7.zip"
            urllib.request.urlretrieve(url, path_to_zip)

        with zipfile.ZipFile(path_to_zip, 'r') as zip_ref:
            zip_ref.extractall("temp/")


def generate_vowl(config):
    """Generate VOWL specifications."""
    # Note: The flag "add-opens" below fixes an issue with
    # "InaccessibleObjectException" in later versions of Java
    for ontology in config["ontologies"]:
        source = ontology["source"]
        basename = os.path.basename(source).split(".")[0]
        path = ontology["path"]
        version = ontology["version"]
        os.system(f"mkdir -p docs/webvowl/data/{path}/{version}/")
        os.system(f"""
            java -Dlog4j.configurationFile=log4j2.xml \
                --add-opens java.base/java.lang=ALL-UNNAMED \
                -jar temp/owl2vowl.jar \
                -file {source} \
                -output docs/webvowl/data/{path}/{version}/{basename}.json > /dev/null
        """)

def main():
    with open("config.yml", 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    copy_ontologies(config)
    download_owl2vowl()
    generate_vowl(config)

if __name__ == "__main__":
    main()