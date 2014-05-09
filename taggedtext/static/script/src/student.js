TaggedText.StudentView = function () {
    this.constructor.apply(this, arguments);
};

TaggedText.StudentView.prototype = {
    constructor: function (server, runtime, element) {
        this.runtime = runtime;
        this.server = server;
        this.element = $(element);
    },

    setupEvents: function () {
        var that = this;
        var keywords = this.element.find('.keyword');

        keywords.click(function () {
            $(this)
                .toggleClass('active')
                .find('.dropdown')
                .toggle();
            keywords.not(this).removeClass('active').find('.dropdown').hide();
        });

        this.element.find('.dropdown > li').click(function () {
            var el = $(this);
            var color = el.find('span');
            var keyword = el.closest('.keyword');

            that.server.selectCategory({
                keyword: keyword.data('position'),
                category: el.data('id')
            }).done(function (data) {
                keyword.css({
                    'background-color': color.css('background-color')
                });
                for (var c in data.counts) {
                    var el = that.element.find('.category-' + c + ' .count');
                    el.text(data.counts[c]);
                }
            }).fail(function (/*msg*/) {
                // TODO: show error
            });
        });
    },

    render: function () {
        this.setupEvents();
    }
};
