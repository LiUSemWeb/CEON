#!/usr/bin/env python3
from pybars import Compiler
from bs4 import BeautifulSoup, formatter
from glob import glob
import os
import re
import urllib.request
import zipfile
from pylode.profiles.vocpub import VocPub
from rdflib import Graph
import logging
from playwright.sync_api import sync_playwright

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
        latest = {}
        # publish ontologies
        for source in sorted(glob(f"ontology/{type}/*/*/*", recursive=True)):
            if not source.endswith(".ttl"):
                continue
            
            parts = re.match(f"ontology/{type}/([^/]*)/([^/]*)", source)    
            name = parts.group(1)
            version = parts.group(2)
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
            
            if latest.get(name, "0") < version:
                latest[name] = version
            
        # add latest
        for name, version in latest.items():
            os.makedirs(f"docs/{map[type]}/{name}/latest/", exist_ok=True)
            os.system(f"cp docs/{map[type]}/{name}/{version}/* docs/{map[type]}/{name}/latest/")


def download_owl2vowl():
    """Download and extract OWL2VOWL."""
    os.system("mkdir -p temp")
    path_to_jar = "temp/owl2vowl.jar"
    if not os.path.isfile(path_to_jar):
        path_to_zip = "temp/owl2vowl_0.3.7.zip"
        if not os.path.isfile(path_to_zip):
            url = "https://github.com/VisualDataWeb/OWL2VOWL/archive/refs/tags/0.3.7.zip"
            urllib.request.urlretrieve(url, path_to_zip)

        with zipfile.ZipFile(path_to_zip, 'r') as zip_ref:
            zip_ref.extractall("temp/")


def generate_vowl():
    """Generate VOWL specifications."""
    map = {
        "modules": "ontology",
        "demo": "demo"
    }

    for type in ["modules", "demo"]:
        for source in sorted(glob(f"ontology/{type}/*/*/*", recursive=True)):
            if not source.endswith(".ttl"):
                continue
            
            logger.info(f"Generating VOWL for: {source}")

            parts = re.match(f"ontology/{type}/([^/]*)/([^/]*)", source)    
            name = parts.group(1)
            version = parts.group(2)
            target = f"docs/webvowl/data/{map[type]}/{name}/{version}/"
            os.makedirs(target, exist_ok=True)
            
            logging.debug(f"Source:\t{source}")
            logging.debug(f"Name:\t{name}")
            logging.debug(f"Target:\t{target}")
            logging.debug(f"Output:\t{target}{name}.json")
            
            # Note: The flag "add-opens" below fixes an issue with
            # "InaccessibleObjectException" in later versions of Java
            os.system(f"""
                java -Dlog4j.configurationFile=log4j2.xml \
                    --add-opens java.base/java.lang=ALL-UNNAMED \
                    -jar temp/owl2vowl.jar \
                    -file {source} \
                    -output {target}{name}.json > /dev/null
            """)


def create_documentation():
    """Generate LODE documentation and instert VOWL visualization."""
    map = {
        "modules": "ontology",
        "demo": "demo"
    }

    for type in ["modules", "demo"]:
        for source in sorted(glob(f"ontology/{type}/*/*/*", recursive=True)):
            if not source.endswith(".ttl"):
                continue
            
            logger.debug(f"Generating docs for {source}")

            parts = re.match(f"ontology/{type}/([^/]*)/([^/]*)", source)    
            name = parts.group(1)
            version = parts.group(2)
            target = f"docs/{map[type]}/{name}/{version}/"
            os.makedirs(target, exist_ok=True)
                    
            html_file = f"{target}/index.html"
            od = VocPub(ontology=source)
            od.make_html(destination=html_file)

            # relative path to webvowl and vowl file
            path_to_webvowl = f"../../../webvowl/index.html#{map[type]}/{name}/{version}/{name}"

            # # Insert overview section into documentation with WebVOWL in an iframe
            with open(html_file, encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                overview = BeautifulSoup(
                    f"""
                    <div id="overview" class="section">
                        <style>
                            #iframe-overview {{
                                width: 100%;
                                height: 600px;
                            }}
                            .caption {{
                                display: flex;
                                justify-content: space-between;
                            }}
                            .caption a {{
                                text-decoration: none;
                                color: black;
                                font-size: 2em;
                            }}
                        </style>
                        <h2>Overview</h2>
                        <div class="figure">
                            <iframe id="iframe-overview" src="{path_to_webvowl}">
                            </iframe>
                            <div class="caption">
                                <div>
                                    <strong>Figure 1:</strong> Ontology overview.
                                </div>
                                <div>
                                    <a title="Show fullscreen" href="{path_to_webvowl}">&#x26F6;</a>
                                </div>
                            </div>
                        </div>
                    </div>
                """, "html.parser")
                tag = soup.find(id='metadata')
                tag.insert_after(overview)

                html_formatter = formatter.HTMLFormatter(indent=4)
                with open(html_file, "w") as f:
                    f.write(soup.prettify(formatter=html_formatter))


def create_index_file():
    print("Generating index file")
    compiler = Compiler()
    template_file = "index.hbs"
    index_file = "docs/index.html"
    
    core = ["actor", "actorODP", "cvn",
            "material", "process", "processODP", "plan",
            "product", "resourceODP", "value", 
            "energy", "quantity", "statement", "location", "datasheet", "full"]
    
    core_actor = ["actorODP", "actor"]
    core_process = ["processODP", "process", "plan"]
    core_resource = ["resourceODP", "material", "product", "energy"]
    core_cvn = ["cvn", "value"]
    core_full = ["full"]
    core_supplementary = ["quantity", "statement", "location", "datasheet"]
    
    data = {
        "core": [],
        "other": [],
        "demo": [],
        "actor": [],
        "process": [],
        "resource": [],
        "cvn": [],
        "full": [],
        "supplementary": []
    }
    for type in ["modules", "demo"]:
        ontologies = {}
        for source in glob(f"ontology/{type}/*/*/*", recursive=True):
            if not source.endswith(".ttl"):
                continue
            parts = re.match(f"ontology/{type}/([^/]*)/([^/]*)", source)    
            name = parts.group(1)
            version = parts.group(2)
            
            if not ontologies.get(name):
                ontologies[name] = {
                    "name": name,
                    "versions": []
                }
            
            ontologies[name]["versions"].append(version)
            ontologies[name]["versions"].sort(reverse=True)
        
        # Split into core, other and demo
        for name in ontologies:
            ontology = {
                "name": name,
                "versions": ontologies[name]["versions"]
            }
            if type == "demo":
                data["demo"].append(ontology)
            else:
                if name in core:
                    data["core"].append(ontology)
                    # New added code below
                    if name in core_actor:
                        data["actor"].append(ontology)
                    if name in core_process:
                        data["process"].append(ontology)
                    if name in core_resource:
                        data["resource"].append(ontology)
                    if name in core_full:
                        data["full"].append(ontology)
                    if name in core_cvn:
                        data["cvn"].append(ontology)
                    if name in core_supplementary:
                        data["supplementary"].append(ontology)
                else:
                    data["other"].append(ontology)
    
    for list in data.values():           
        list.sort(key=lambda x: x["name"])

    # sort by name ascending, version descending
    with open(template_file, "r") as f:
        template = compiler.compile(f.read())
        
    with open(index_file, "w") as f:
        f.write(template({"data": data}))

def html_to_pdf_with_playwright(html_file, pdf_file):
    """Convert HTML file to a PDF file using Playwright."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # Load the HTML file
            page.goto(f"file://{os.path.abspath(html_file)}")

            # Generate PDF
            page.pdf(path=pdf_file, format="A4", margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}, scale=0.7)
            browser.close()
    except Exception as e:
        logger.error(f"Failed to generate PDF for {html_file}: {e}")


def build_pdf_playwright():
    """Convert docs to PDF using Playwright."""
    try:
        html_formatter = formatter.HTMLFormatter(indent=4)
        map = {
            "modules": "ontology",
            "demo": "demo"
        }

        for type in ["modules", "demo"]:
            for source in sorted(glob(f"ontology/{type}/*/*/*", recursive=True)):
                if not source.endswith(".ttl"):
                    continue

                logger.info(f"Generating PDF docs for {source}")

                parts = re.match(f"ontology/{type}/([^/]*)/([^/]*)", source)    
                name = parts.group(1)
                version = parts.group(2)
            
                target = f"docs/{map[type]}/{name}/{version}/"
                html_file = f"{target}/index.html"
                pdf_file = f"{target}/{name}.pdf"
                
                # Drop TOC, logo, and iframe before generating PDF 
                with open(html_file, encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    style = soup.new_tag('style', type='text/css')
                    style.append("""
                        /* hack to avoid lonely heading (most of the time at least) */
                        h2 {
                            page-break-inside: avoid;
                        }
                        .section h2::after {
                            content: "";
                            display: block;
                            height: 300px;
                            margin-bottom: -300px;
                        }
                        .entity {
                            page-break-inside: avoid;
                        }
                        p, dt, dd, ul {
                            margin-top: 10px;
                            margin-bottom: 10px;
                            padding-top: 0;
                            padding-bottom: 0;
                        }
                    """)
                    soup.head.append(style)
                    
                    for id in ["toc", "pylode", "overview"]:
                        tag = soup.find(id=id)
                        if tag is not None:
                            tag.decompose()
                
                # Write modified HTML back to temp file
                temp_file = "temp/html_to_pdf.html"
                with open(temp_file, "w", encoding="utf-8") as f:
                   f.write(soup.prettify(formatter=html_formatter))
                
                # Generate PDF using Playwright
                html_to_pdf_with_playwright(temp_file, pdf_file)
    except Exception as e:
        logger.error(e)
        logger.error("PDF conversion cancelled. Ensure Playwright is installed and configured properly.")


def main():
    download_owl2vowl()
    generate_vowl()
    create_documentation()
    build_pdf_playwright()
    create_index_file()
    copy_ontologies()

if __name__ == "__main__":
    main()
