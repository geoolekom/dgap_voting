$( ".panel-heading" ).click(function () {
    var panel_body = $(this).parent().find(".panel-body");
    panel_body.toggle("fold");
});
