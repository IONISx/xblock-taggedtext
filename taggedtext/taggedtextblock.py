import json

from jinja2 import Template
from lxml import etree

from xblock.core import XBlock
from xblock.fields import Scope, List, Dict, String, Integer
from xblock.fragment import Fragment

from taggedtext.settings_mixin import SettingsMixin
from taggedtext.student_mixin import StudentMixin
from taggedtext.studio_mixin import StudioMixin
from taggedtext.xml import update_from_xml


class TaggedTextXBlock(
    XBlock,
    SettingsMixin,
    StudentMixin,
    StudioMixin):

    title = String(
        default="",
        scope=Scope.content,
        help="Title of the block (plain text)"
    )

    prompt = String(
        default="",
        scope=Scope.content,
        help="Prompt of the block (plain text)"
    )

    default_score = Integer(
        default=1,
        scope=Scope.content,
        help="Default score for a point"
    )

    categories = List(
        scope=Scope.content,
        help="Categories"
    )

    fragments = List(
        scope=Scope.content,
        help="Fragments"
    )

    @classmethod
    def parse_xml(cls, node, runtime, keys, id_generator):
        """
        Instantiate XBlock object from runtime XML definition.
        """
        block = runtime.construct_xblock_from_class(cls, keys)

        return update_from_xml(block, node)

    @classmethod
    def generate_color(cls, text, pos, count):
        return 'hsl({}, 62%, 82%)'.format((pos) * (255 / count))

    @XBlock.json_handler
    def select_category(self, data, suffix=''):
        category = data.get('value')
        keyword = str(data.get('id'))
        if category in self.categories:
            self.student_answer[keyword] = category
        return data

    @XBlock.json_handler
    def check(self, data, suffix=''):
        pass

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
</vertical_demo>""") ]
