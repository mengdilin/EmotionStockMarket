function capitalize(str){
    var pieces = str.split(" ");
    for ( var i = 0; i < pieces.length; i++ )
    {
        var j = pieces[i].charAt(0).toUpperCase();
        pieces[i] = j + pieces[i].substr(1);
    }
    return pieces.join(" ");
}
function removeApos(t){
    res=""
    for (var i=0;i<t.length;i++){
	res=res+t[i];
    }
    return res
}
function fillEventsBefore(Borough,Month,Day,Year){
    var stuff ={}
    stuff.Month=Month
    stuff.Day=Day
    stuff.Year=Year
    stuff.Borough=Borough
    $.getJSON("/get_e_before",stuff,function(data){
	var l=$("#events");
	var event=$("ol")
	$(l).append(event);
	for (var i in data){
	    //console.log(i);
	    var title=capitalize(data[i][8].toLowerCase()).split("'")
	    title=removeApos(title);
	    var name="<a href='http://www.google.com/#hl=en&tbo=d&output=search&sclient=psy-ab&q="+title+"'>"+"<h2>"+capitalize(data[i][8].toLowerCase())+"</h2>"+"</a>";
	    var d="<p> Description: "+data[i][10];
	    var dte="<p> Date: "+data[i][12];
	    var loc="<p> Location: "+data[i][18];
	    event=$("<ol></ol>");
	    event.append(name);
	    event.append(d);
	    event.append(dte);
	    event.append(loc);
	    $(event).attr("href","http://www.google.com");
	    $(event).css('color','gray');
	    $('a',event).css('color','gray');
	    $(l).append(event);
	}
    });
};

function fillEventsOn(Borough,Month,Day,Year){
    var stuff ={}
    stuff.Month=Month
    stuff.Day=Day
    stuff.Year=Year
    stuff.Borough=Borough
    $.getJSON("/get_e_on",stuff,function(data){
	//console.log("here");
	var l=$("#events");
	l.empty();
	var event=$("ol")
	$(l).append(event);
	for (var i in data){
	    //console.log(i);
	    //var name="<h2>"+capitalize(data[i][8].toLowerCase())+"</h2>";
	    var title=capitalize(data[i][8].toLowerCase()).split("'")
	    title=removeApos(title);
	    console.log(title);
	    var name="<a href='http://www.google.com/#hl=en&tbo=d&output=search&sclient=psy-ab&q="+title+"'>"+"<h2>"+capitalize(data[i][8].toLowerCase())+"</h2>"+"</a>";
	    var d="<p> Description: "+data[i][10];
	    var dte="<p> Date: "+data[i][12];
	    var loc="<p> Location: "+data[i][18];
	    event=$("<ol></ol>");
	    event.append(name);
	    event.append(d);
	    event.append(dte);
	    event.append(loc);
	    $(event).attr("href","http://www.google.com");
	    $(event).css('color','red');
	    $('a',event).css('color','red');
	    $(l).append(event);
	}
    });
    fillEventsAfter(Borough,Month,Day,Year);
};

function fillEventsAfter(Borough,Month,Day,Year){
    var stuff ={}
    stuff.Month=Month
    stuff.Day=Day
    stuff.Year=Year
    stuff.Borough=Borough
    $.getJSON("/get_e_after",stuff,function(data){
	var l=$("#events");
	var event=$("ol")
	$(l).append(event);
	for (var i in data){
	    //var name="<h2>"+capitalize(data[i][8].toLowerCase())+"</h2>";
	    var title=capitalize(data[i][8].toLowerCase()).split("'")
	    title=removeApos(title);
	    var name="<a href='http://www.google.com/#hl=en&tbo=d&output=search&sclient=psy-ab&q="+title+"'>"+"<h2>"+capitalize(data[i][8].toLowerCase())+"</h2>"+"</a>";
	    var d="<p> Description: "+data[i][10];
	    var dte="<p> Date: "+data[i][12];
	    var loc="<p> Location: "+data[i][18];
	    event=$("<ol></ol>");
	    event.append(name);
	    event.append(d);
	    event.append(dte);
	    event.append(loc);
	    $(event).attr("href","http://www.google.com");
	    $(event).css('color','blue');
	    $('a',event).css('color','blue');
	    $(l).append(event);
	}
    });
    fillEventsBefore(Borough,Month,Day,Year);
};
/* in maps.js:
function display(b){
    console.log(b);
    if (b=="Staten Island"){
	b="SI"
    }
    var nimage = $("#"+b).attr("src");
    console.log(image)
    $("#image").attr("src",nimage)
    
}
*/
function varyB(data){
    var borough="";
    borough=$(this).val();
    var month=$("select[name='Month']").val();
    var day=$("select[name='Day']").val();
    var year=$("select[name='Year']").val();
    fillEventsOn(borough,month,day,year);
    //display(borough)
}
function varyM(data){
    var month="";
    month =$(this).val();
    var borough=$("#Borough").val();
    var day=$("select[name='Day']").val();
    var year=$("select[name='Year']").val();
    fillEventsOn(borough,month,day,year);
}
function varyD(data){
    var day="";
    day=$(this).val();
    var month=$("select[name='Month']").val();
    var borough=$("#Borough").val();
    var year=$("select[name='Year']").val();
    fillEventsOn(borough,month,day,year);
}
function varyY(data){
    var year="";
    year=$(this).val();
    var month=$("select[name='Month']").val();
    var day=$("select[name='Day']").val();
    var borough=$("#Borough").val();
    fillEventsOn(borough,month,day,year);
}
function loadEvents(){
    $("#Borough").change(varyB);
}
function DateTime(){
    $("select[name='Month']").change(varyM);
    $("select[name='Day']").change(varyD);
    $("select[name='Year']").change(varyY);
    //var month=$("select[name='Month']").val();
    //var day=$("select[name='Day']").val();
    //var year=$("select[name='Year']").val();
    //var borough=$("#Borough").val();
    //fillEventsOn(borough,month,day,year);
}

$(document).ready(function(){
    loadEvents();
    DateTime();
});
