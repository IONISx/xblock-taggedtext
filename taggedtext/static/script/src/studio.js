TaggedText.StudioView = function () {
    this.constructor.apply(this, arguments);
};

TaggedText.StudioView.prototype = {
    constructor: function (server, runtime, element) {
        this.runtime = runtime;
        this.server = server;
        this.element = $(element);
        this.xmlEditor = null;
    },

    load: function () {
        var that = this;

        this.server.loadXml().done(
            function (data) {
                that.xmlEditor.setValue(data);
            }).fail(function (msg) {
                that.showError(msg);
            }
        );
    },

    save: function () {
        if (!this.xmlEditor) {
            this.showError('View not rendered yet, cannot save');
            return;
        }

       var xml = this.xmlEditor.getValue();

        this.runtime.notify('save', {
            state: 'start'
        });

        var that = this;
        this.server.updateXml(xml).done(function() {
            that.runtime.notify('save', {
                state: 'end'
            });

            that.load();
        }).fail(function (msg) {
            that.showError(msg);
        });
    },

    cancel: function () {
        this.runtime.notify('cancel', {});
    },

    showError: function (msg) {
        this.runtime.notify('error', {
            msg: msg
        });
    },

    setupEvents: function () {
        var that = this;

        this.element.find('.taggedtext-save-button').click(function () {
            that.save();
        });
        this.element.find('.taggedtext-cancel-button').click(function () {
            that.cancel();
        });
    },

    render: function () {
        this.xmlEditor = CodeMirror.fromTextArea(
            this.element.find('.taggedtext-editor').get(0), {
                mode: 'xml',
                lineNumbers: true,
                lineWrapping: true
            }
        );
        this.setupEvents();
        this.load();
    }
};
