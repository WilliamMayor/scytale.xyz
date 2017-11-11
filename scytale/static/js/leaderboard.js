$("body.leaderboard").ready(function() {
    $("a.toggle").click(function() {
        $(this).parents(".group").find(".points").toggleClass("hidden");
        return false;
    });
});
