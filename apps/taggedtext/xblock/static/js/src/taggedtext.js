function TaggedTextXBlock(runtime, element) {

    var selectCategoryUrl = runtime.handlerUrl(element, 'select_category');
    var checkUrl = runtime.handlerUrl(element, 'check');

    var tags = $('.tag', element);

    tags.click(function (e) {
        $(this)
            .toggleClass('active')
            .find('.dropdown')
            .toggle();
        tags.not(this).removeClass('active').find('.dropdown').hide();
    });

    $('.dropdown > li', element).click(function (e) {
        e.preventDefault();

        var el = $(this);
        var color = $(this).find('span');
        var tag = el.closest('.tag');
        tag.css({
            'background-color': color.css('background-color')
        });

        $.post(selectCategoryUrl, JSON.stringify({
            id: tag.data('position'),
            value: el.data('id')
        }), function (data) {
            tag.removeClass('active').find('.dropdown').hide();
        });
    });

    $('.check', element).click(function (e) {
        $.post(checkUrl, JSON.stringify({}), function (data) {
            console.log(data);
        });
    });
}
