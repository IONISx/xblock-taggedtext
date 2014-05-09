"""
Studio editing view for TaggedText XBlock
"""

import json

from xblock.core import XBlock
from xblock.fragment import Fragment

from taggedtext.utils import load_resource, render_template
from taggedtext.xml import update_from_xml_str, serialize_content, UpdateFromXmlError, ValidationError


class StudioMixin(object):
    """
    Studio editing view for Tagged Text XBlock
    """

    def studio_view(self, context=None):
        """
        Method to render the Tagged Text XBlock in Studio
        """

        data = {
            'metadata_fields': json.dumps(self.editable_metadata_fields)
        }

        template = render_template('templates/studio.html', data)
        frag = Fragment(template)
        frag.add_javascript(load_resource('static/script/xblock-taggedtext.min.js'))
        frag.initialize_js('TaggedTextXBlockStudio')
        return frag

    @XBlock.json_handler
    def update_xml(self, data, suffix=''):
        """
        Update the XBlock's XML.
        """
        if 'xml' in data:
            try:
                update_from_xml_str(self, data['xml'])

            except ValidationError as ex:
                return {'success': False, 'msg': 'Validation error: {error}'.format(error=ex.message)}

            except UpdateFromXmlError as ex:
                return {'success': False, 'msg': 'An error occurred while saving: {error}'.format(error=ex.message)}

            else:
                return {'success': True, 'msg': 'Successfully updated TaggedText XBlock'}

        else:
            return {'success': False, 'msg': 'Must specify "xml" in request JSON dict.'}

    @XBlock.json_handler
    def xml(self, data, suffix=''):
        """
        Retrieve the XBlock's content definition, serialized as XML.
        """
        try:
            xml = serialize_content(self)
        except Exception as ex:
            msg = 'An unexpected error occurred while loading the problem: {error}'.format(error=ex)
            return {'success': False, 'msg': msg, 'xml': u''}
        else:
            return {'success': True, 'msg': '', 'xml': xml}
