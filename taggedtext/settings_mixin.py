"""
Settings for TaggedText XBlock
"""

from xblock.core import XBlock
from xblock.fields import Scope, String, Float, Integer, List, Dict

from taggedtext.defaults import DISPLAY_NAME


class SettingsMixin(object):
    """
    Settings for TaggedText XBlock
    """

    display_name = String(
        default=DISPLAY_NAME,
        display_name="Display Name",
        scope=Scope.settings,
        help="This name appears in the horizontal navigation at the top of the page."
    )

    max_attempts = Integer(
        default=None,
        display_name="Maximum Attempts",
        values={"min": 0},
        scope=Scope.settings,
        help=("Defines the number of times a student can try to answer this problem. "
              "If the value is not set, infinite attempts are allowed.")
    )

    weight = Float(
        display_name="Problem Weight",
        values={"min": 0, "step": .1},
        scope=Scope.settings,
        help=("Defines the number of points each problem is worth. "
              "If the value is not set, each response field in the problem is worth one point.")
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
            self.get_keyword_score(fragment)
            for fragment in self.fragments if fragment['type'] == 'keyword'
        )

    @property
    def non_editable_metadata_fields(self):
        """
        Return the list of fields that should not be editable in Studio.
        """
        return [XBlock.tags, XBlock.name]

    @property
    def editable_metadata_fields(self):
        """
        Returns the metadata fields to be edited in Studio. These are fields with scope `Scope.settings`.
        """
        def jsonify_value(field, json_choice):
            if isinstance(json_choice, dict) and 'value' in json_choice:
                json_choice = dict(json_choice)  # make a copy so below doesn't change the original
                json_choice['value'] = field.to_json(json_choice['value'])
            else:
                json_choice = field.to_json(json_choice)
                return json_choice

        metadata_fields = {}

        # Only use the fields from this class, not mixins
        fields = getattr(self, 'unmixed_class', self.__class__).fields

        for field in fields.values():
            if field.scope != Scope.settings or field in self.non_editable_metadata_fields:
                continue

            # gets the 'default_value' and 'explicitly_set' attrs
            metadata_fields[field.name] = self.runtime.get_field_provenance(self, field)
            metadata_fields[field.name]['field_name'] = field.name
            metadata_fields[field.name]['display_name'] = field.display_name
            metadata_fields[field.name]['help'] = field.help
            metadata_fields[field.name]['value'] = field.read_json(self)

            # We support the following editors:
            # 1. A select editor for fields with a list of possible values (includes Booleans).
            # 2. Number editors for integers and floats.
            # 3. A generic string editor for anything else (editing JSON representation of the value).
            editor_type = "Generic"
            values = field.values
            if isinstance(values, (tuple, list)) and len(values) > 0:
                editor_type = "Select"
                values = [jsonify_value(field, json_choice) for json_choice in values]
            elif isinstance(field, Integer):
                editor_type = "Integer"
            elif isinstance(field, Float):
                editor_type = "Float"
            elif isinstance(field, List):
                editor_type = "List"
            elif isinstance(field, Dict):
                editor_type = "Dict"

            metadata_fields[field.name]['type'] = editor_type
            metadata_fields[field.name]['options'] = [] if values is None else values

        return metadata_fields
