from xblock.core import XBlock
from xblock.fields import Scope, List, String, Integer

import taggedtext.defaults as defaults
from taggedtext.grading_mixin import GradingMixin
from taggedtext.settings_mixin import SettingsMixin
from taggedtext.student_mixin import StudentMixin
from taggedtext.studio_mixin import StudioMixin
from taggedtext.xml_parsing import update_from_xml_node, serialize_content_to_xml


class TaggedTextXBlock(
        XBlock,
        GradingMixin,
        SettingsMixin,
        StudentMixin,
        StudioMixin):

    title = String(
        default=defaults.TITLE,
        scope=Scope.content,
        help="Title of the block (plain text)"
    )

    prompt = String(
        default=defaults.PROMPT,
        scope=Scope.content,
        help="Prompt of the block (plain text)"
    )

    default_score = Integer(
        default=defaults.SCORE,
        scope=Scope.content,
        help="Default score for a point"
    )

    categories = List(
        default=defaults.CATEGORIES,
        scope=Scope.content,
        help="Categories"
    )

    fragments = List(
        default=defaults.FRAGMENTS,
        scope=Scope.content,
        help="Fragments"
    )

    def add_xml_to_node(self, node):
        """
        Serialize the XBlock to XML for exporting.
        """
        serialize_content_to_xml(self, node)

    @classmethod
    def parse_xml(cls, node, runtime, keys, id_generator):
        """
        Instantiate XBlock object from runtime XML definition.
        """
        block = runtime.construct_xblock_from_class(cls, keys)

        return update_from_xml_node(block, node)

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("TaggedTextXBlock",
             """
<vertical_demo>
  <taggedtext>
    <title>Sample TaggedText block</title>
    <categories>
      <category id="la">Latin</category>
      <category id="en">English</category>
      <category id="fr">French</category>
      <category id="ru">Russian</category>
    </categories>
    <text>
       Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut arcu
       nisl, <keyword category="la">luctus</keyword> vel tellus <keyword
       category="la" score="4">id</keyword>, sagittis euismod
       nulla.
       Phasellus quam magna, sagittis non justo ac, viverra
       <keyword category="en">house</keyword> ipsum. Sed bibendum arcu
       et sapien elementum ultricies. <keyword
       category="en">Because</keyword> semper sollicitudin nunc vitae
       pharetra.<keyword category="en">nothing</keyword>
    </text>
  </taggedtext>
</vertical_demo>""")]
