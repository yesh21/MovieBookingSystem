// Enable popover
$(function () {
    $('[data-toggle="popover"]').popover()
})

// Flash message function for page javascript
let flash_message = function (message, category) {
    let new_msg = `<div class="alert alert-${category}">${message} </div>`;
    $('#flashContainer').append(new_msg);
}

// From https://www.w3schools.com/js/js_cookies.asp
function setCookie(cname, cvalue, days_until_expiry) {
    var d = new Date();
    d.setTime(d.getTime() + (days_until_expiry * 24 * 60 * 60 * 1000));
    var expires = 'expires=' + d.toUTCString();
    document.cookie = `${cname}=${cvalue};${expires};path=/`;
}

function setSessionCookie(cname, cvalue) {
    var d = new Date();
    document.cookie = `${cname}=${cvalue};path=/`;
}

// From https://www.w3schools.com/js/js_cookies.asp
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return '';
}

// Cookies warning
$('#cookieDeny').on('click', function () {
    $('#cookieAlert').addClass('d-none');
    setSessionCookie('allow_cookies', 1);
});

$('#cookieAccept').on('click', function () {
    $('#cookieAlert').addClass('d-none');
    setCookie('allow_cookies', 1, 90);
    // Re-enable login remember me
    if ($('#cookiesDisableWarning').length && $('#remember').length) {
        $('#remember').prop('disabled', false);
        $('#cookiesDisableWarning').addClass('d-none');
    }
});

// Show warning if have not accepted
if (getCookie('allow_cookies') === '') {
    $('#cookieAlert').removeClass('d-none');
}

// Search
$(function () {
    $("#searchBox").autocomplete({
        source: function (request, response) {
            $.ajax({
                type: "POST",
                url: "http://localhost:5000/movie/search",
                dataType: "json",
                cache: false,
                data: {
                    q: request.term
                },
                success: function (data) {
                    //alert(data);
                    //console.log(data);
                    response(data);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus + " " + errorThrown);
                }
            });
        },
        minLength: 2
    });
});