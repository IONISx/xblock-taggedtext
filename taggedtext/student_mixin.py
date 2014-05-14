"""
Student view for TaggedText XBlock
"""

import json
from copy import deepcopy
from xblock.core import XBlock
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

    def get_student_answer(self, keyword):
        return self.student_answer.get(str(keyword['position']))

    def generate_color(self, pos, count):
        return 'hsl({}, 62%, 82%)'.format((pos) * (255 / count))

    def student_view(self, context=None):
        """
        The primary view of the TaggedTextXBlock, shown to students
        when viewing courses.
        """

        categories = deepcopy(self.categories)
        categories_count = len(categories)
        state = self.get_problem_state()

        for i, c in enumerate(categories):
            if 'color' not in c:
                c['color'] = self.generate_color(i, categories_count)

        fragments = deepcopy(self.fragments)
        keywords = (f for f in fragments if f['type'] == 'keyword')

        for keyword in keywords:
            answer = next((a for a in state['answers'] if a['position'] == keyword['position']))
            if answer['answer']:
                keyword['color'] = next((c for c in categories if c['id'] == answer['answer']))['color']

        data = {
            'fragments': fragments,
            'categories': categories,
            'title': self.title,
            'prompt': self.prompt,
            'attempts_used': self.attempts,
            'attempts_allowed': self.max_attempts,
            'state': json.dumps(state)
        }

        template = render_template('templates/student.html', data)
        frag = Fragment(template)
        frag.add_css(load_resource('static/style/xblock-taggedtext.min.css'))
        frag.add_javascript(load_resource('static/script/xblock-taggedtext.min.js'))
        frag.initialize_js('TaggedTextXBlockStudent')
        return frag

    @XBlock.json_handler
    def select_category(self, data, suffix=''):
        if self.problem_locked:
            return {'success': False, 'msg': "Problem can't be answered anymore"}

        keyword_text = unicode(data.get('keyword'))
        category_text = data.get('category')

        if keyword_text in self.graded_answers:
            self.graded_answers.remove(keyword_text)

        category = next((c for c in self.categories if c['id'] == category_text), None)
        if category:
            self.student_answer[keyword_text] = category['id']

            state = self.get_problem_state()
            return {'success': True, 'state': state}

        return {'success': False, 'msg': "No such category '{}'".format(category)}
