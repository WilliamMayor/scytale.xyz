$("body.messages.read").ready(function() {
    $("a.toggle-group").click(function() {
        $(this).parents(".group").find(".message").toggleClass("hidden");
        return false;
    });
    $("a.toggle-message").click(function() {
        $(this).parents(".message").find(".details").toggleClass("hidden");
        return false;
    });
});
