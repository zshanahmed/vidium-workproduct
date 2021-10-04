function validateChrom() {
    const start = document.getElementById("chromosome_start");
    const end = document.getElementById("chromosome_end");
    const div = document.getElementById("alert");
    div.className="";
    if (end.value && (end.value < start.value)) {
        div.className = "note";
        div.innerHTML = "*Chromosome end cannot be less than chromosome start";
    } else
    {
        div.innerHTML="";
    }
}