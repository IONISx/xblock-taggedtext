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
        var keywords = this.element.find('.keyword');

        keywords.click(function (e) {
            $(this)
                .toggleClass('active')
                .find('.dropdown')
                .toggle();
            keywords.not(this).removeClass('active').find('.dropdown').hide();
        });
    },

    render: function () {
        this.setupEvents();
    }
};
