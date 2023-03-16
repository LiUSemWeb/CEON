#!/usr/bin/env python3
from pybars import Compiler
from bs4 import BeautifulSoup, formatter
import os
import yaml
import urllib.request
import zipfile

def copy_ontologies(config):
    """Copy ontologies to web path."""
    for ontology in config["ontologies"]:
        source = ontology["source"]
        path = ontology["path"]
        version = ontology["version"]
        os.system(f"mkdir -p docs/{path}/{version}")
        os.system(f"cp {source} docs/{path}/{version}/")


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
        path = ontology["path"]
        version = ontology["version"]
        basename = os.path.basename(source).split(".")[0]
        os.system(f"mkdir -p docs/webvowl/data/{path}/{version}/")
        os.system(f"""
            java -Dlog4j.configurationFile=log4j2.xml \
                --add-opens java.base/java.lang=ALL-UNNAMED \
                -jar temp/owl2vowl.jar \
                -file {source} \
                -output docs/webvowl/data/{path}/{version}/{basename}.json > /dev/null
        """)


def create_documentation(config):
    """Generate LODE documentation and instert VOWL visualization."""
    for ontology in config["ontologies"]:
        source = ontology["source"]
        basename = os.path.basename(source).split(".")[0]
        path = ontology["path"].strip("/")
        version = ontology["version"].strip("/")
        
        os.system(f"mkdir -p docs/{path}/{version}/")
        
        # Note: Using the pyLODE package as a module is not working fails,
        # and we instead call it using the CLI method
        html_file = f"docs/{path}/{version}/index.html"
        os.system(f"python3 -m pylode {source} -o {html_file}")      

        # relative path to webvowl
        rel = "../" * f"{path}/{version}/".count("/")
        path_to_webvowl = rel + f"webvowl/index.html#{path}/{version}/{basename}"

        # Insert overview section into documentation with WebVOWL in an iframe
        with open(html_file, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            overview = BeautifulSoup(f"""
                <div id="overview" class="section">
                    <h2>Overview</h2>
                    <div class="figure">
                        <iframe id="iframe-overview" width="100%" height ="800px" src="{path_to_webvowl}"></iframe>
                        <div class="caption"><strong>Figure 1:</strong> Ontology overview</div>
                    </div>
                </section>
            """, "html.parser")
            tag = soup.find(id='metadata')
            tag.insert_after(overview)
        
        html_formatter = formatter.HTMLFormatter(indent=4)
        with open(html_file, "w") as f:
            f.write(soup.prettify(formatter=html_formatter))


def create_index_file(config):
        compiler = Compiler()
        template_file = "index.hbs"
        index_file = "docs/index.html"
        
        data = []
        for ontology in config["ontologies"]:
            source = ontology["source"]
            path = ontology["path"].strip("/")
            version = ontology["version"].strip("/")
            basename = os.path.basename(source)
            data.append({"docs": f"{path}/{version}/index.html",
                         "file": f"{path}/{version}/{basename}",
                         "version": version,
                         "title": basename})
        
        # sort by name ascending, version descending
        data.sort(key=lambda x: (x["title"], -float(x["version"])))
        with open(template_file, "r") as f:
            template = compiler.compile(f.read())
            
        with open(index_file, "w") as f:
            f.write(template({"data": data}))

def main():
    with open("config.yml", 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    copy_ontologies(config)
    download_owl2vowl()
    generate_vowl(config)
    create_documentation(config)
    create_index_file(config)


if __name__ == "__main__":
    main()