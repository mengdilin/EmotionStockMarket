function display(data){
    //console.log(b);
    b=$(this).val()
    if (b=="Staten Island"){
	b="SI"
    }
    var nimage = $("#"+b).attr("src");
    console.log(image)
    $("#image").attr("src",nimage)
    
}
function loadImage(){
    $("#Borough").change(display);
}
$(document).ready(function(){
    loadImage();
});