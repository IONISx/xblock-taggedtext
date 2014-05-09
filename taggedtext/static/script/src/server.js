TaggedText.Server = function () {
    this.constructor.apply(this, arguments);
};

TaggedText.Server.prototype = {
    constructor: function (runtime, element) {
        this.runtime = runtime;
        this.element = element;
    },

    url: function (handler) {
        return this.runtime.handlerUrl(this.element, handler);
    },

    selectCategory: function (options) {
        var url = this.url('select_category');
        var payload = JSON.stringify({
            keyword: options.keyword,
            category: options.category
        });

        return $.Deferred(function (defer) {
            $.ajax({
                type: 'POST',
                url: url,
                data: payload
            }).done(function (data) {
                if (data.success) {
                    defer.resolve();
                }
                else {
                    defer.rejectWith(this, [data.msg]);
                }
            }).fail(function () {
                defer.rejectWith(this, ['Could not save the selected category']);
            });
        }).promise();
    },

    edit: function (data) {
        var url = this.url('edit');
        var payload = JSON.stringify(data);

        return $.Deferred(function (defer) {
            $.ajax({
                type: 'POST',
                url: url,
                data: payload
            }).done(function (data) {
                if (data.success) {
                    defer.resolve();
                }
                else {
                    defer.rejectWith(this, [data.msg]);
                }
            }).fail(function () {
                defer.rejectWith(this, ['This problem could not be saved.']);
            });
        }).promise();
    },

    loadXml: function() {
        var url = this.url('xml');

        return $.Deferred(function (defer) {
            $.ajax({
                type: 'POST',
                url: url,
                data: JSON.stringify(null)
            }).done(function (data) {
                if (data.success) {
                    defer.resolveWith(this, [data.xml]);
                }
                else {
                    defer.rejectWith(this, [data.msg]);
                }
            }).fail(function () {
                defer.rejectWith(this, ['This problem could not be loaded.']);
            });
        }).promise();
    }
};
