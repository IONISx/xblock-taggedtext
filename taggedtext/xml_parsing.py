"""
Serialize and deserialize TaggedText XBlock content to/from XML.
"""

import lxml.etree as etree
import xml.dom.minidom as md


class UpdateFromXmlError(Exception):
    """
    Error occurred while deserializing the TaggedText XBlock content from XML.
    """
    pass


class ValidationError(UpdateFromXmlError):
    """
    The XML definition is not semantically valid.
    """
    pass


def _safe_get_text(element):
    """
    Retrieve the text from the element, safely handling empty elements.
    """
    return u' '.join(t.nodeValue for t in element.childNodes if t.nodeType == t.TEXT_NODE)


def _parse_categories_xml(categories_root):
    """
    Parse <categories> element in the TaggedText XBlock's content XML.
    """
    categories_list = []

    for category in categories_root.getElementsByTagName('category'):
        category_dict = dict()

        # retrieve id
        if category.hasAttribute('id'):
            category_dict['id'] = unicode(category.getAttribute('id'))
        else:
            raise UpdateFromXmlError("XML category definition must contain a 'id' attribute.")

        category_dict['name'] = _safe_get_text(category)

        # retrieve color (optional)
        if category.hasAttribute('color'):
            category_dict['color'] = unicode(category.getAttribute('color'))

        # retrieve description (optional)
        if category.hasAttribute('description'):
            category_dict['description'] = unicode(category.getAttribute('description'))

        categories_list.append(category_dict)

    return categories_list


def _parse_keyword_xml(keyword):
    """
    Parse <keyword> element in the TaggedText XBlock's content XML.
    """
    keyword_dict = dict()

    # retrieve category
    if keyword.hasAttribute('category'):
        keyword_dict['category'] = unicode(keyword.getAttribute('category'))
    else:
        raise UpdateFromXmlError("XML keyword definition must contain a 'category' attribute.")

    # retrieve text
    keyword_dict['text'] = _safe_get_text(keyword)

    # retrieve score (optional)
    if keyword.hasAttribute('score'):
        keyword_dict['score'] = int(keyword.getAttribute('score'))

    return keyword_dict


def _parse_text_xml(text_root):
    """
    Parse <text> element in the TaggedText XBlock's content XML.
    """
    fragments_list = []
    keywords_count = 0

    for node in text_root.childNodes:
        if node.nodeType == node.TEXT_NODE:
            fragments_list.append({
                'type': 'text',
                'text': unicode(node.nodeValue)
            })
        elif node.nodeName == 'keyword':
            keyword_dict = _parse_keyword_xml(node)
            keyword_dict.update({
                'type': 'keyword',
                'position': keywords_count
            })
            fragments_list.append(keyword_dict)
            keywords_count += 1

    return fragments_list


def serialize_content_to_xml(block, root):
    """
    Serialize the TaggedText XBlock's content to XML.
    """
    root.tag = 'taggedtext'

    # set title
    title = etree.SubElement(root, 'title')
    title.text = unicode(block.title)

    # set prompt
    prompt = etree.SubElement(root, 'prompt')
    prompt.text = unicode(block.prompt)

    # set categories
    categories_root = etree.SubElement(root, 'categories')
    for category_dict in block.categories:
        category = etree.SubElement(categories_root, 'category')

        category.set('id', unicode(category_dict['id']))
        category.text = unicode(category_dict['name'])

        if 'color' in category_dict:
            category.set('color', unicode(category_dict['color']))

        if 'description' in category_dict:
            category.set('description', unicode(category_dict['description']))

    # set text
    text_root = etree.SubElement(root, 'text')
    for fragment_dict in block.fragments:
        if fragment_dict['type'] == 'keyword':
            keyword = etree.SubElement(text_root, 'keyword')

            keyword.set('category', unicode(fragment_dict['category']))
            keyword.text = unicode(fragment_dict['text'])

            if 'score' in fragment_dict:
                keyword.set('score', unicode(fragment_dict['score']))

        elif fragment_dict['type'] == 'text':
            children = text_root.getchildren()

            if not children:
                text_root.text = unicode(fragment_dict['text'])

            else:
                children[-1].tail = unicode(fragment_dict['text'])


def serialize_content(block):
    """
    Serialize the TaggedText XBlock's content to an XML string.
    """
    root = etree.Element('taggedtext')
    serialize_content_to_xml(block, root)

    return etree.tostring(root, pretty_print=True, encoding='utf-8')


def update_from_xml(block, root):
    """
    Update the TaggedText XBlock's content from an XML definition.
    """
    if root.tagName != 'taggedtext':
        raise UpdateFromXmlError("XML content must contain an 'taggedtext' root element.")

    # retrieve title
    title_el = root.getElementsByTagName('title')
    if title_el is None or len(title_el) != 1:
        raise UpdateFromXmlError("XML content must contain a 'title' element.")

    title = _safe_get_text(title_el[0])

    # retrieve prompt
    prompt_el = root.getElementsByTagName('prompt')
    if prompt_el is None or len(prompt_el) != 1:
        raise UpdateFromXmlError("XML content must contain a 'prompt' element.")

    prompt = _safe_get_text(prompt_el[0])

    # retrieve categories
    categories_el = root.getElementsByTagName('categories')
    if categories_el is None or len(categories_el) != 1:
        raise UpdateFromXmlError("XML content must contain a 'categories' element.")

    categories = _parse_categories_xml(categories_el[0])

    # parse text
    text_el = root.getElementsByTagName('text')
    if text_el is None or len(text_el) != 1:
        raise UpdateFromXmlError("XML content must contain a 'text' element.")

    fragments = _parse_text_xml(text_el[0])

    print fragments

    block.title = title
    block.prompt = prompt
    block.categories = categories
    block.fragments = fragments

    return block

def update_from_xml_str(block, xml):
    """
    Update the TaggedText XBlock's content from an XML string definition.
    """
    try:
        dom = md.parseString(xml.encode('utf-8'))
    except Exception:
        raise UpdateFromXmlError("An error occurred while parsing the XML content.")

    return update_from_xml(block, dom.documentElement)

def update_from_xml_node(block, node):
    string = etree.tostring(node, encoding='utf-8')

    return update_from_xml_str(block, string)
