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

    updateXml: function (xml) {
        var url = this.url('update_xml');
        var payload = JSON.stringify({
            xml: xml
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
