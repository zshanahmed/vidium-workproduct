function validateChrom() {
    const start = document.getElementById("chromosome_start");
    const end = document.getElementById("chromosome_end");
    const div = document.getElementById("alert");
    div.className="";
    if (end.value && (end.value < start.value)) {
        console.log(end.value);
        div.className = "note";
        div.innerHTML = "*Chromosome end cannot be less than chromosome start";
    } else
    {
        div.innerHTML="";
    }
}

function validateAF(){
    const afValue = document.querySelector('#af_cutoff').value;
    const small = document.querySelector('#af-note');
    if (afValue > 1){
        small.textContent = '*AF Value cannot be greater than 1';
        small.className = 'note';
    } else {
        small.textContent = "";
    }
}

(function ($) {

    $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0].name;
        $('#uploadCsvLabel').text(fileName);
    });
    
    
})(jQuery);