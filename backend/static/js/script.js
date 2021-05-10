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
    var a = document.createElement('a');
    a.href = hit.url;
    a.target="_blank";
    a.appendChild(document.createTextNode("Go to code"));
    td.appendChild(a);
    tr.appendChild(td);

    var td = document.createElement('td');
    for (j = 0; j < hit.methods.length; j++) {
        var p = document.createElement('p');
        var pre = document.createElement('pre');
        pre.style = "word-wrap: break-word; white-space: pre-wrap;"
        pre.appendChild(document.createTextNode(hit.methods[j]));
        p.appendChild(pre);
        td.append(p);
    }
    tr.appendChild(td);

    results.appendChild(tr);
}
