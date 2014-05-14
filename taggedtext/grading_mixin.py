"""
Grading for TaggedText XBlock
"""

from xblock.core import XBlock
from xblock.fields import Scope, List, Integer, Boolean


class GradingMixin(object):
    """
    Grading for TaggedText XBlock
    """

    attempts = Integer(
        default=0,
        scope=Scope.user_state,
        help="Number of attempts taken by the student on this problem"
    )

    graded_answers = List(
        scope=Scope.user_state,
        help="Graded student answers"
    )

    resolved = Boolean(
        default=False,
        scope=Scope.user_state,
        help="Defines whether the problem has been resolved"
    )

    @property
    def problem_locked(self):
        return self.resolved or self.max_attempts is not None and self.attempts >= self.max_attempts

    def get_keyword_score(self, keyword):
        return keyword['score'] if 'score' in keyword else self.default_score

    def get_problem_state(self):
        answers_list = []

        keywords = (f for f in self.fragments if f['type'] == 'keyword')

        for keyword in keywords:
            answer = self.get_student_answer(keyword)
            keyword_position = keyword['position']
            graded = unicode(keyword_position) in self.graded_answers

            answer_dict = {
                'answer': answer,
                'max_score': self.get_keyword_score(keyword),
                'position': keyword_position,
                'graded': graded
            }

            if self.problem_locked:
                answer_dict['real_answer'] = keyword['category']

            if graded:
                correct = answer == keyword['category']
                answer_dict['score'] = self.get_keyword_score(keyword) if correct else 0
                answer_dict['correct'] = correct

            answers_list.append(answer_dict)

        any_graded = any(a['graded'] for a in answers_list)
        global_max_score = sum(a['max_score'] for a in answers_list)

        data = {
            'graded': any_graded,
            'answers': answers_list,
            'max_score': global_max_score,
            'attempts': self.attempts,
            'max_attempts': self.max_attempts,
            'counts': dict(),
            'locked': self.problem_locked,
        }

        for c in self.categories:
            data['counts'][c['id']] = len([v for v in self.student_answer.values() if v == c['id']])

        if any_graded:
            data['resolved'] = self.resolved
            data['score'] = sum(a.get('score', 0) for a in answers_list)

        return data

    @XBlock.json_handler
    def check(self, data, suffix=''):
        if self.problem_locked:
            return {'success': False, 'msg': 'Cannot grade problem anymore'}

        self.attempts += 1

        for answer in self.student_answer:
            if answer not in self.graded_answers:
                self.graded_answers.append(answer)

        self.resolved = all((
            self.student_answer.get(unicode(f['position'])) == f['category']
            for f in self.fragments if f['type'] == 'keyword'
        ))

        return {
            'success': True,
            'state': self.get_problem_state()
        }
