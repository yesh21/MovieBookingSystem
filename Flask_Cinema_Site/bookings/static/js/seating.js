$(document).ready(function () {
    var hide = document.getElementById("PaymentsButton");
    hide.style.display = "none";

    var currentSeats = [];
    $('.btn').on('click', function (event) {
        current = $(this).attr('id');
        if (!$(this).hasClass("disabled")) {
            if (currentSeats.find(element => element == current) != undefined) {
                $(this).removeClass("btn-danger");
                $(this).addClass("btn-info");
                currentSeats.splice(currentSeats.findIndex(element => element == current), 1);
                //testSize();
            } else if (currentSeats.find(element => element == current) == undefined) {
                $(this).removeClass("btn-info");
                $(this).addClass("btn-danger");
                currentSeats.push(current);
                //testSize();
            }

            var x = document.getElementById("PaymentsButton");
            if (currentSeats.length > 0) {
                x.style.display = "block";
            } else if (currentSeats.length == 0) {
                x.style.display = "none";
            }
        }
    });

    $("#PaymentsButton").on("click", function () {
        //Now submit seat booked


        $.ajax({
            url: '/book/slot/seats',
            type: 'POST',
            data: JSON.stringify(currentSeats),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function () {
                console.log("success")
                var link = window.location.origin
                window.location.href = link + "/book/pay";
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});