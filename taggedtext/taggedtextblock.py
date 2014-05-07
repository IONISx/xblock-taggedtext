import json

from jinja2 import Template
from lxml import etree

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, List, Dict, String, Integer
from xblock.fragment import Fragment

from taggedtext.lms_mixin import LmsMixin
from taggedtext.studio_mixin import StudioMixin


class TaggedTextXBlock(
    XBlock,
    LmsMixin,
    StudioMixin):

    title = String(
        default="",
        scope=Scope.content,
        help="Title of the block (plain text)"
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

    student_answer = Dict(
        scope=Scope.user_state,
        help="Student answers"
    )

    has_score = True
    icon_class = 'problem'

    # @classmethod
    # def parse_xml(cls, node, runtime, keys, id_generator):
    #     block = runtime.construct_xblock_from_class(cls, keys)

    #     for child in node:
    #         tag = child.tag.lower()
    #         if tag == u'categories':
    #             cls.extract_categories(block, child)
    #         if tag == u'text':
    #             cls.extract_keywords(block, child)

    #             block.rich_text = []

    #             block.rich_text.append({
    #                 'type': 'text',
    #                 'text': node.text
    #             })

    #             cls.extract_text(block, child)



    #     print block.keywords
    #     print block.rich_text
    #     return block

    @classmethod
    def generate_color(cls, text, pos, count):
        return 'hsl({}, 62%, 82%)'.format((pos) * (255 / count))

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


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
