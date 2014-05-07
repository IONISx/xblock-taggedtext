/* jshint unused: false */

function TaggedTextXBlockStudio(runtime, element) {
    $(function () {
        var server = new TaggedText.Server(runtime, element);
        var view = new TaggedText.StudioView(server, runtime, element);
        view.render();
    });
}

function TaggedTextXBlockStudent(runtime, element) {
    $(function () {
        var server = new TaggedText.Server(runtime, element);
        var view = new TaggedText.StudentView(server, runtime, element);
        view.render();
    });
}
