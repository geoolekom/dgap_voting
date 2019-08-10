jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

/* Move following code to servertime app*/
function serverTime() {
    var time = null;
    $.ajax({url: $('#defaultTime').attr("data-url-servertime"),
        async: false, dataType: 'text',
        success: function(text) {
            time = new Date(text);
        }, error: function(http, message, exc) {
            time = new Date();
    }});
    return time;
}

function serverDate() {
    var time = null;
    $.ajax({url: $('#defaultTime').attr("data-url-serverdate"),
        async: false, dataType: 'text',
        success: function(text) {
            time = new Date(text);
        }, error: function(http, message, exc) {
            time = new Date();
    }});
    return time;
}

$(function () {
    var startDay = serverDate();
    $('#defaultTime').countdown({since: startDay, compact: true, format: 'HMS', description: '', serverSync: serverTime});
});
