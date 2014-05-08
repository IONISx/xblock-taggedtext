"""
Serialize and deserialize TaggedText XBlock content to/from XML.
"""

import lxml.etree as etree


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
    return unicode(element.text) if element.text is not None else u""


def _parse_categories_xml(categories_root):
    """
    Parse <categories> element in the TaggedText XBlock's content XML.
    """
    categories_list = []

    for category in categories_root.findall('category'):
        category_dict = dict()

        # retrieve id
        if 'id' in category.attrib:
            category_dict['id'] = unicode(category.get('id'))
        else:
            raise UpdateFromXmlError("XML category definition must contain a 'id' attribute.")

        # retrieve name
        if category.text:
            category_dict['name'] = _safe_get_text(category)
        else:
            raise UpdateFromXmlError("XML category definition must contain the name of the category.")

        # retrieve color (optional)
        if 'color' in category.attrib:
            category_dict['color'] = unicode(category.get('color'))

        # retrieve description (optional)
        if 'description' in category.attrib:
            category_dict['description'] = unicode(category.get('description'))

        categories_list.append(category_dict)

    return categories_list


def _parse_keyword_xml(keyword_el):
    """
    Parse <keyword> element in the TaggedText XBlock's content XML.
    """
    keyword_dict = dict()

    # retrieve category
    if 'category' in keyword_el.attrib:
        keyword_dict['category'] = unicode(keyword_el.get('category'))
    else:
        raise UpdateFromXmlError("XML keyword definition must contain a 'category' attribute.")

    # retrieve text
    if keyword_el.text:
        keyword_dict['text'] = _safe_get_text(keyword_el)
    else:
        raise UpdateFromXmlError("XML keyword definition must contain the text of the keyword.")

    # retrieve score (optional)
    if 'score' in keyword_el.attrib:
        keyword_dict['score'] = int(keyword_el.get('score'))

    return keyword_dict


def _parse_text_xml(nodes):
    """
    Parse <text> element in the TaggedText XBlock's content XML.
    """
    fragments_list = []
    keywords_count = 0

    for item in nodes:
        if isinstance(item, (str,unicode)):
            fragments_list.append({
                'type': 'text',
                'text': unicode(item)
            })
        elif isinstance(item, (etree._Element,)):
            if item.tag == 'keyword':
                keyword_dict = _parse_keyword_xml(item)
                keyword_dict['type'] = 'keyword'
                keyword_dict['position'] = keywords_count
                fragments_list.append(keyword_dict)
                keywords_count += 1
            else:
                fragments_list.append({
                    'type': 'text',
                    'text': etree.tostring(item, with_tail=False)
                })

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
    if root.tag != 'taggedtext':
        raise UpdateFromXmlError("XML content must contain an 'taggedtext' root element.")

    # retrieve title
    title_el = root.find('title')
    if title_el is None:
        raise UpdateFromXmlError("XML content must contain a 'title' element.")

    title = _safe_get_text(title_el)

    # retrieve prompt
    prompt_el = root.find('prompt')
    if prompt_el is None:
        raise UpdateFromXmlError("XML content must contain a 'prompt' element.")

    prompt = _safe_get_text(prompt_el)

    # retrieve categories
    categories_el = root.find('categories')
    if categories_el is None:
        raise UpdateFromXmlError("XML content must contain a 'categories' element.")

    categories = _parse_categories_xml(categories_el)

    # parse text
    text_el = root.find('text')
    if text_el is None:
        raise UpdateFromXmlError("XML content must contain a 'text' element.")

    fragments = _parse_text_xml(root.xpath('/taggedtext/text/node()'))

    block.title = title
    block.prompt = prompt
    block.categories = categories
    block.fragments = fragments

    return block


def update_from_xml_str(block, xml, **kwargs):
    """
    Update the TaggedText XBlock's content from an XML string definition.
    """
    try:
        root = etree.fromstring(xml.encode('utf-8'))
    except (ValueError, etree.ParseError):
        raise UpdateFromXmlError("An error occurred while parsing the XML content.")

    return update_from_xml(block, root, **kwargs)
