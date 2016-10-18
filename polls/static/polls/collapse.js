$( ".panel-heading" ).click(function () {
    var panel_body = this.parent().find(".panel-body");
    if (panel_body.is(":visible")) {
        panel_body.hide();
        alert("LOL");
    } else {
        panel_body.show();
    }
});