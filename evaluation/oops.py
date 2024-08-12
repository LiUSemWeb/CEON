from rdflib import Graph, RDF, URIRef
from bs4 import BeautifulSoup, formatter
import requests
from glob import glob
import re
import sys

def main(filter=[]):
    oops_url = "https://oops.linkeddata.es/rest"
    oops_req_template = """
    <?xml version="1.0" encoding="UTF-8"?>
    <OOPSRequest>
        <OntologyURI>{0}</OntologyURI>
        <OntologyContent></OntologyContent>
        <Pitfalls></Pitfalls>
        <OutputFormat>RDF/XML</OutputFormat>
    </OOPSRequest>
    """

    # Define the HTML output format  
    html_output = """
        <html>
            <head>
                <title>OOPS! Report Summary</title>
                <link href="css/bootstrap.min.css" rel="stylesheet"/>
                <link href="css/dataTables.bootstrap5.css" rel="stylesheet"/>
                <script src="js/jquery-3.7.1.js"></script>
                <script src="js/bootstrap.bundle.min.js"></script>
                <script src="js/dataTables.js"></script>
                <script src="js/dataTables.bootstrap5.js"></script>
                <link href="css/style.css" rel="stylesheet"/>
            </head>
            <script>
                window.onload = () => {
                    $('#oops-table thead tr')
                        .clone(true)
                        .addClass('filters')
                        .appendTo('#oops-table thead');
                        
                    let table = $('#oops-table').DataTable({
                            orderCellsTop: true,
                            pageLength: 50,
                            initComplete: function () {
                                let api = this.api();
                    
                                // For each column
                                api
                                    .columns()
                                    .eq(0)
                                    .each(function (colIdx) {
                                        // Set the header cell to contain the input element
                                        let cell = $('.filters th').eq(
                                            $(api.column(colIdx).header()).index()
                                        );
                                        let title = $(cell).text().trim();
                                        $(cell).html('<input type="text" placeholder="' + title + '" />');
                    
                                        // On every keypress in this input
                                        $(
                                            'input',
                                            $('.filters th').eq($(api.column(colIdx).header()).index())
                                        )
                                            .off('keyup change')
                                            .on('change', function (e) {
                                                // Get the search value
                                                $(this).attr('title', $(this).val());
                                                let regexr = '({search})'; //$(this).parents('th').find('select').val();
                    
                                                let cursorPosition = this.selectionStart;
                                                // Search the column for that value
                                                api
                                                    .column(colIdx)
                                                    .search(
                                                        this.value != ''
                                                            ? regexr.replace('{search}', '(((' + this.value + ')))')
                                                            : '',
                                                        this.value != '',
                                                        this.value == ''
                                                    )
                                                    .draw();
                                            })
                                            .on('keyup', function (e) {
                                                e.stopPropagation();
                    
                                                $(this).trigger('change');
                                                $(this)
                                                    .focus()[0]
                                                    .setSelectionRange(cursorPosition, cursorPosition);
                                            });
                                    });
                            },
                        });
                }
            </script>
        <body>
        <h1>OOPS! Report Summary</h1>
        <table id="oops-table" class="table table-striped table-hover dataTable" width="100%">
        <thead>
            <tr>
                <th>Module</th>
                <th>Pitfall Name</th>
                <th>Code</th>
                <th>Level</th>
                <th>Affected Elements</th>
            </tr>
        </thead>
        <tbody>"""

    modules = {}
    for source in glob("ontology/modules/*/*/*", recursive=True):
        parts = re.match("ontology/modules/([^/]*)/([^/]*)", source)    
        name = parts.group(1)
        
        if len(filter) > 0 and name not in filter:
            continue
        
        version = parts.group(2)
        
        if not modules.get(name):
            modules[name] = []
        
        modules[name].append(version)

    modules = [f"{name}/{max(versions)}/" for name, versions in modules.items()]
    modules.sort()

    ceon_prefix = "http://w3id.org/CEON/ontology/"
    for module in modules:
        module_url = f"{ceon_prefix}{module}"
        print(f"Generating OOPS! report for {module_url}")
        resp = requests.post(url=oops_url,
                            data=oops_req_template.format(module_url),
                    allow_redirects=True)

        # Create an rdflib graph and parse the RDF string  
        g = Graph()
        g.parse(data=resp.content, format="xml")
        
        # Loop over all the pitfall instances
        oops = "http://oops.linkeddata.es/def#"
        pitfall_class_uri = URIRef(oops + "pitfall")  
        for pitfall_instance in g.subjects(RDF.type, pitfall_class_uri):  
            # Look up the data properties for the pitfall instance  
            pitfall_name = g.value(pitfall_instance, URIRef(oops + "hasName"))
            pitfall_description = g.value(pitfall_instance, URIRef(oops + "hasDescription"))
            pitfall_code = g.value(pitfall_instance, URIRef(oops + "hasCode"))  
            pitfall_importance_level = g.value(pitfall_instance, URIRef(oops + "hasImportanceLevel")) 
            affected_elements = []  
            for affected_element in g.objects(pitfall_instance, URIRef(oops + "hasAffectedElement")):  
                affected_element_label = str(affected_element)  
                affected_elements.append(affected_element_label) 
                
            # Add a row to the HTML table for the pitfall instance  
            html_output += f"""
                <tr>
                    <td>{module}</td>
                    <td title=\"{pitfall_description}\">{pitfall_name}</td>
                    <td>{pitfall_code}</td>
                    <td>{pitfall_importance_level}</td>
                    <td>{',<br>'.join(affected_elements)}</td>
                </tr>""" 
            # Finish the table output  

    html_output += "</tbody></table>"
        
    # Finish HTML
    html_output += "</body></html>"  


    # Print the HTML output
    html_formatter = formatter.HTMLFormatter(indent=4)
    with open("evaluation/oops.html", "w") as f:
        soup = BeautifulSoup(html_output, "html.parser")
        f.write(soup.prettify(formatter=html_formatter))
        

if __name__ == "__main__":
    filter = sys.argv[1:]
    main(filter)