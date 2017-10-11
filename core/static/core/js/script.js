jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

function serverTime() {
    var time = null;
    $.ajax({url: "{% url 'servertime:server_time' %}",
        async: false, dataType: 'text',
        success: function(text) {
            time = new Date(text);
        }, error: function(http, message, exc) {
            time = new Date();
    }});
    return time;
};
function serverDate() {
    var time = null;
    $.ajax({url: "{% url 'servertime:server_date' %}",
        async: false, dataType: 'text',
        success: function(text) {
            time = new Date(text);
        }, error: function(http, message, exc) {
            time = new Date();
    }});
    return time;
};

$(function () {
        var startDay = serverDate();
        $('#defaultTime').countdown({since: startDay, compact: true, format: 'HMS', description: '', serverSync: serverTime});
});
