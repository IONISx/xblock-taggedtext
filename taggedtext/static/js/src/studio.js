TaggedText.StudioView = function () {
    this.constructor.apply(this, arguments);
};

TaggedText.StudioView.prototype = {
    constructor: function (runtime) {
        this.runtime = runtime;
    },

    save: function () {
        this.updateXml();
    },

    cancel: function () {
        this.runtime.notify('cancel', {});
    },

    render: function (element) {
        element = $(element);

        this.xmlEditor = CodeMirror.fromTextArea(
            element.find('.taggedtext-editor').get(0), {
                mode: 'xml',
                lineNumbers: true,
                lineWrapping: true
            }
        );

        var that = this;
        element.find('.taggedtext-save-button').click(function () {
            that.save();
        });
        element.find('.taggedtext-cancel-button').click(function () {
            that.cancel();
        });
    }
};
