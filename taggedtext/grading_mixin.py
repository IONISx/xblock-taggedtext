"""
Grading for TaggedText XBlock
"""

from xblock.core import XBlock


class GradingMixin(object):
    """
    Grading for TaggedText XBlock
    """

    def get_keyword_score(self, keyword):
        return keyword['score'] if 'score' in keyword else self.default_score

    @XBlock.json_handler
    def check(self, data, suffix=''):
        answers_list = []

        keywords = (f for f in self.fragments if f['type'] == 'keyword')

        for keyword in keywords:
            answer = self.get_student_answer(keyword)
            correct = answer == keyword['category']
            answers_list.append({
                'answer': answer,
                'score': self.get_keyword_score(keyword) if correct else 0,
                'max_score': self.get_keyword_score(keyword),
                'correct': correct,
                'position': keyword['position']
            })

        global_correct = all(a['correct'] for a in answers_list)
        global_score = sum(a['score'] for a in answers_list)
        global_max_score = sum(a['max_score'] for a in answers_list)

        return {
            'success': True,
            'answers': answers_list,
            'correct': global_correct,
            'score': global_score,
            'max_score': global_max_score
        }
