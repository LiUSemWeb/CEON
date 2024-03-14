from rdflib import Graph, RDF, URIRef
from bs4 import BeautifulSoup, formatter
import requests
from glob import glob
import re
import json

def main(filter=[]):
    foops_url = "https://foops.linkeddata.es/assessOntology"

    # Define the HTML output format  
    html_output = """
        <html>
            <head>
                <title>FOOPS! Report Summary</title>
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
        <h1>FOOPS! Report Summary</h1>
        <table id="oops-table" class="table table-striped table-hover dataTable" width="100%">
        <thead>
            <tr>
                <th>Module</th>
                <th>Principle ID</th>
                <th>Category ID</th>
                <th>Status</th>
                <th>Title</th>
                <th>Explanation</th>
                <th>Total passed tests</th>
                <th>Total tests run</th>
            </tr>
        </thead>
        <tbody>"""

    modules = {}
    for source in glob("ontology/modules/*/*/*", recursive=True):
        parts = re.match("ontology/modules/([^/]*)/([^/]*)", source)    
        name = parts.group(1)
                
        if len(filter) > 0 and name not in filter:
            continue
        
        version = float(parts.group(2))
        if not modules.get(name):
            modules[name] = []
        
        modules[name].append(version)

    modules = [f"{name}/{max(versions)}/" for name, versions in modules.items()]
    modules.sort()

    ceon_prefix = "https://w3id.org/CEON/ontology/"
    for module in modules:
        module_url = f"{ceon_prefix}{module}"
        print(f"Generating FOOPS! report for {module_url}")
        resp = requests.post(url=foops_url,
                            data=f"{{\"ontologyUri\": \"{module_url}\"}}",
                            headers={ "Content-Type": "application/json" },
                            allow_redirects=True)

        d = json.loads(resp.content)

        for check in d["checks"]:
            id = check["id"]
            principle_id = check["principle_id"]
            category_id = check["category_id"]
            status = check["status"]
            title = check["title"]
            explanation = check["explanation"]
            description = check["description"]
            total_passed_tests = check["total_passed_tests"]
            total_tests_run = check["total_tests_run"]
            
            html_output += f"""
                <tr>
                    <td>{module}</td>
                    <td>{principle_id}</td>
                    <td>{category_id}</td>
                    <td>{status}</td>
                    <td title="{description}">{title}</td>
                    <td>{explanation}</td>
                    <td>{total_passed_tests}</td>
                    <td>{total_tests_run}</td>
                </tr>""" 
        # Finish the table output  

    html_output += "</tbody></table>"
        
    # Finish HTML
    html_output += "</body></html>"  


    # Print the HTML output
    html_formatter = formatter.HTMLFormatter(indent=4)
    with open("evaluation/foops.html", "w") as f:
        soup = BeautifulSoup(html_output, "html.parser")
        f.write(soup.prettify(formatter=html_formatter))
    
if __name__ == "__main__":
    main()