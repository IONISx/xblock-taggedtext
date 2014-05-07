"""
Settings for TaggedText XBlock
"""

from xblock.fields import String, Float, Scope

class SettingsMixin(object):
    """
    Settings for TaggedText XBlock
    """

    display_name = String(
        default="Tagged Text",
        scope=Scope.settings,
        help="Display name"
    )

    weight = Float(
        display_name="Problem Weight",
        values={"min": 0, "step": .1},
        scope=Scope.settings,
        help="Problem weight"
    )

    def has_dynamic_children(self):
        return False

    @property
    def icon_class(self):
        return 'problem'

    @property
    def has_score(self):
        return True


    def max_score(self):
        return sum(
            fragment['score'] or self.default_score
            for fragment in self.fragments if fragment['type'] == 'keyword'
        )
