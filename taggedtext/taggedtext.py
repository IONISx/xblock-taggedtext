"""TO-DO: Write a description of what this XBlock is."""

import json

from copy import deepcopy
from jinja2 import Template
from lxml import etree

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, List, Dict, String, Integer
from xblock.fragment import Fragment


class TaggedTextXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    has_score = True
    icon_class = 'problem'

    categories = Dict(
        scope=Scope.content,
        help="Categories"
    )

    rich_text = List(
        scope=Scope.content,
        help="Text that will be tagged later on"
    )

    keywords = List(
        scope=Scope.content,
        help="List of keywords"
    )

    default_score = Integer(
        default=1, scope=Scope.content,
        help="Default score for a point"
    )

    student_answer = Dict(
        scope=Scope.user_state,
        help="Student answers"
    )

    @classmethod
    def parse_xml(cls, node, runtime, keys, id_generator):
        block = runtime.construct_xblock_from_class(cls, keys)

        for child in node:
            tag = child.tag.lower()
            if tag == u'categories':
                cls.extract_categories(block, child)
            if tag == u'text':
                cls.extract_keywords(block, child)

                block.rich_text = []

                block.rich_text.append({
                    'type': 'text',
                    'text': node.text
                })

                cls.extract_text(block, child)



        print block.keywords
        print block.rich_text
        return block

    @classmethod
    def generate_color(cls, text, pos, count):
        return 'hsl({}, 62%, 82%)'.format((pos) * (255 / count))

    @classmethod
    def extract_categories(cls, block, node):
        categories = [n for n in node if n.tag.lower() == u'category']
        count = len(categories)
        for pos, child in enumerate(categories):
            id = child.get('id')
            if id:
                block.categories[id] = {
                    'name': child.text,
                    'description': child.get('description') or '',
                    'color': child.get('color') or cls.generate_color(id, pos, count)
                }

    @classmethod
    def extract_keywords(cls, block, node):
        block.keywords = []

        for element in node.iter('keyword'):
            block.keywords.append({
                'category': element.get('category'),
                'score': int(element.get('score', block.default_score)),
                'text': element.text
            })


    @classmethod
    def extract_text(cls, block, node):
        for element in node.iterchildren():
            if element.tag == u'keyword':
                block.rich_text.append({
                    'type': 'keyword',
                    'position': len([e for e in block.rich_text if e['type'] == 'keyword']),
                    'text': element.text
                })
                block.rich_text.append({
                    'type': 'text',
                    'text': element.tail
                })
            else:
                block.rich_text.append({
                    'type': 'text',
                    'text': element.text
                })
                cls.extract_text(block, element)


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the TaggedTextXBlock, shown to students
        when viewing courses.
        """

        keywords = deepcopy(self.keywords)
        for pos, k in enumerate(keywords):
            answer = self.student_answer.get(str(pos))
            if answer:
                k['answer'] = answer

        data = {
            'rich_text': self.rich_text,
            'keywords': keywords,
            'categories': self.categories
        }

        template = Template(self.resource_string("static/html/taggedtext.html"))
        frag = Fragment(template.render(data))

        frag.add_css(self.resource_string("static/css/taggedtext.css"))
        frag.add_javascript(self.resource_string("static/js/src/taggedtext.js"))
        frag.initialize_js('TaggedTextXBlock')
        return frag


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
    <categories>
      <category id="la">Latin</category>
      <category id="en">English</category>
      <category id="fr">French</category>
      <category id="ru">Russian</category>
    </categories>
    <text>
      <p>
       Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut arcu
       nisl, <keyword category="la">luctus</keyword> vel tellus <keyword
       category="la" score="4">id</keyword>, sagittis euismod
       nulla.<br/>
      </p>
      <p>
       Phasellus quam magna, sagittis non justo ac, viverra
       <keyword category="en">house</keyword> ipsum. Sed bibendum arcu
       et sapien elementum ultricies. <keyword
       category="en">Because</keyword> semper sollicitudin nunc vitae
       pharetra.<keyword category="en">nothing</keyword>
      </p>
    </text>
  </taggedtext>
</vertical_demo>""") ]
