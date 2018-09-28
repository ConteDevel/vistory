$.fn.isInViewport = function() {
    var elementTop = $(this).offset().top;
    var elementBottom = elementTop + $(this).outerHeight();
    var viewportTop = $(window).scrollTop();
    var viewportBottom = viewportTop + $(window).height();
    return elementBottom < viewportBottom;
};

$(function() {
    $(".navbar-burger").click(function() {
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    });
    var offset = $('#rightBar').offset().top;
    $(window).scroll(function() {
        if ($('#rightBar').isInViewport()) {
            var scrollTop = $(window).scrollTop();
            $('#rightBar').offset({top: offset + scrollTop});
        }
    });
});