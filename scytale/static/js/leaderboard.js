$("body.leaderboard").ready(function() {
    $("a.toggle").click(function() {
        $(this).parents(".group").next(".points").toggleClass("hidden");
        return false;
    });
});
