"""
Student view for TaggedText XBlock
"""

from copy import deepcopy
from xblock.fields import Scope, Dict
from xblock.fragment import Fragment

from taggedtext.utils import load_resource, render_template


class StudentMixin(object):
    """
    Student view for Tagged Text XBlock
    """

    student_answer = Dict(
        scope=Scope.user_state,
        help="Student answers"
    )

    def student_view(self, context=None):
        """
        The primary view of the TaggedTextXBlock, shown to students
        when viewing courses.
        """

        fragments = deepcopy(self.fragments)
        for f in [f for f in fragments if f['type'] == 'keyword']:
            answer = self.student_answer.get(str(f['position']))
            if answer:
                f['answer'] = answer

        data = {
            'fragments': fragments,
            'categories': self.categories,
            'title': self.title,
            'prompt': self.prompt
        }

        template = render_template('templates/student.html', data)
        frag = Fragment(template)
        frag.add_css(load_resource('static/style/xblock-taggedtext.min.css'))
        frag.add_javascript(load_resource('static/script/xblock-taggedtext.min.js'))
        frag.initialize_js('TaggedTextXBlockStudent');
        return frag
