$(document).ready(function(){
    // Constructs the suggestion engine
    var playerName = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        // The url points to a json file that contains an array of player names
        prefetch: '/playerlist'
    });
    
    // Initializing the typeahead with prefetched data
    $('.typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1,
        //forces first suggestion to be selected
        autoselect: true
    },
     {
        name: 'countries',
        source: playerName,
        limit: 6 /* Specify maximum number of suggestions to be displayed */
    });

});  

//Changes color of font to green and red according to win loss
function winColor() {
    var elements = document.getElementsByClassName("card")
    for (var i=0; i<elements.length; i++) {
        var t1 = 'team' + i + '-0';
        var p1 = t1 + 'pts';
        var t2 =  'team' + i + '-1';
        var p2 = t2 + 'pts';
        var team1 = document.getElementById(p1).innerHTML;
        var team2 = document.getElementById(p2).innerHTML;
        
        if (team1 > team2) 
        {
            document.getElementById(t1).style.color = '#009933';
            document.getElementById(p1).style.color = '#009933';
            document.getElementById(t2).style.color = '#e23434';
            document.getElementById(p2).style.color = '#e23434';
        }
        else
        {
            document.getElementById(t1).style.color = '#e23434';
            document.getElementById(p1).style.color = '#e23434';
            document.getElementById(t2).style.color = '#009933';
            document.getElementById(p2).style.color = '#009933';
        }

    }
};


//Datepicker script
$(function () {
    $('#datetimepicker').datetimepicker({
        format: 'L',
        useCurrent: true,
        maxDate: moment(),
    });
});

function mtd(date){
    return moment(date).subtract(1, 'days').toDate();
};



jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "num-html-pre": function ( a ) {
        var x = String(a).replace( /<[\s\S]*?>/g, "" );
        return parseFloat( x );
    },
 
    "num-html-asc": function ( a, b ) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },
 
    "num-html-desc": function ( a, b ) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
} );