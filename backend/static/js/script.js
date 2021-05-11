if (typeof output !== 'undefined') {
var hits = output.hits;}

var lim;

function get_output(){
    // displays the 10 first output of the query
    lim = 10;
    for (i = 0; i < Math.min(hits.length, lim); i++) {
        display(hits[i]);
    }
    hide_button();
}

function hide_button(){
    // hides the button that displays more results if it is unnecessary
    if (hits.length > lim){
        document.getElementById('seemore').style.visibility='visible';
    }
    else{
        document.getElementById('seemore').style.visibility='hidden';
    }
}

function add_results(){
    // adds results to the list when the button is clicked on
    for (i = lim; i < Math.min(hits.length, lim + 10); i++) {
        display(hits[i]);
    }
    lim = lim + 10;
    hide_button();
}

function display(hit){
    // displays a retrieved result

    var results = document.getElementById('results'); // get appropriate table
    var tr = document.createElement('tr');

    // add name with url link

    var td = document.createElement('td');
    var a = document.createElement('a');
    a.href = hit.url;
    a.target="_blank";
    a.appendChild(document.createTextNode(hit.name));
    td.appendChild(a);
    tr.appendChild(td);

    // add functions

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
