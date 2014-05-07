"""
Student view for TaggedText XBlock
"""

from copy import deepcopy
from xblock.fragment import Fragment

from taggedtext.utils import load_resource, render_template


class LmsMixin(object):
    """
    Student view for Tagged Text XBlock
    """

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
            'categories': self.categories
        }

        template = render_template('templates/student.html', data)
        frag = Fragment(template)
        frag.add_css(load_resource('static/style/xblock-taggedtext.min.css'))
        return frag
