$(document).ready(function() {
    $(".btn").click(function(){
        if($("#Banner1").hasClass("d-none")){
            $("#Banner1").removeClass("d-none")
            $("#Banner2").addClass("d-none")
        } else{
            $("#Banner2").removeClass("d-none")
            $("#Banner1").addClass("d-none")
        }
    });

});