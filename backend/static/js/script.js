if (typeof output !== 'undefined') {
var hits = output.hits;}


function get_output(){
    for (i = 0; i < Math.min(hits.length, 10); i++) {
        display(hits[i]);
    }
}

function display(hit){
    var results = document.getElementById('results');
    var tr = document.createElement('tr');

    var td = document.createElement('td');
    td.appendChild(document.createTextNode(hit.name));
    tr.appendChild(td);

    var td = document.createElement('td');
    td.appendChild(document.createTextNode(hit.url));
    tr.appendChild(td);

    var td = document.createElement('td');
    td.appendChild(document.createTextNode(hit.method_or_class));
    tr.appendChild(td);

    var td = document.createElement('td');
    td.appendChild(document.createTextNode(hit.codeblock));
    tr.appendChild(td);

    results.appendChild(tr);
}
