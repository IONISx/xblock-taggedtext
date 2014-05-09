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
    def edit(self, data, suffix=''):
        """
        Update the XBlock's XML.
        """
        if 'xml' not in data:
            return {'success': False, 'msg': 'Must specify "xml" in request JSON dict.'}
        try:
            update_from_xml_str(self, data['xml'])

        except ValidationError as ex:
            return {'success': False, 'msg': 'Validation error: {error}'.format(error=ex.message)}

        except UpdateFromXmlError as ex:
            return {'success': False, 'msg': 'An error occurred while saving: {error}'.format(error=ex.message)}

        if 'metadata' not in data:
            return {'success': False, 'msg': 'Must specify "metadata" in request JSON dict.'}

        editable_fields = self.editable_metadata_fields

        for metadata_key, metadata in data['metadata'].items():
            if metadata_key not in self.fields:
                return {'success': False, 'msg': 'Field "{name}" does not exist'.format(name=metadata_key)}

            if metadata_key not in editable_fields:
                return {'success': False, 'msg': 'Field "{name}" is not editable'.format(name=metadata_key)}

            value = metadata.get('value')
            field = self.fields[metadata_key]

            if value is None:
                field.delete_from(self)
            else:
                try:
                    value = field.from_json(value)
                except ValueError:
                    return {'success': False, 'msg': 'Invalid data for field {name}'.format(name=metadata_key)}

                field.write_to(self, value)

        return {'success': True, 'msg': 'Successfully updated TaggedText XBlock'}

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
