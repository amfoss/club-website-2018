    $(window).load(function () {
        //resize just happened, pixels changed
        if ($(window).width() < 737) {
            $("#btn-home").addClass('fa-angle-down').removeClass('fa-angle-right');
        }
        else {
            $("#btn-home").addClass('fa-angle-right').removeClass('fa-angle-down');
        }
    });