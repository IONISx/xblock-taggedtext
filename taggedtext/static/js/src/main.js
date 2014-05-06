if (typeof TaggedText === 'undefined' || !TaggedText) {
    TaggedText = {};
}

// XBlock entry points:

TaggedTextXBlockStudio = function (runtime, element) {
    $(function () {
        var view = new TaggedText.StudioView(runtime);
        view.render(element);
    });
};
