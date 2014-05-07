/* jshint unused: false */

function TaggedTextXBlockStudio(runtime, element) {
    $(function () {
        var server = new TaggedText.Server(runtime, element);
        var view = new TaggedText.StudioView(server, runtime);
        view.render(element);
    });
}
