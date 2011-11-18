from django.forms import Widget
from django.forms.util import flatatt
from django.template.loader import render_to_string

from shared.Parser import get_parser
from shared.trackers import DATA_TYPES
from shared.trackers.datasources.factory import get_datasource

class ValuePickerWidget(Widget):

    class Media:
        css = {'all': ('css/value_picker.css',)}
        js = ('js/value_picker.js',)

    input_type = 'text'
    templates_name = 'trackers_wiz/widgets/%s_picker.html'

    def render(self, name, value, attrs=None):
        data_type = self.attrs['data_type']
        content = self.attrs['grabbed_data']
        del self.attrs['data_type']
        del self.attrs['grabbed_data']

        render_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value is None:
            value = ''
        else:
            render_attrs['value'] = value

        if data_type == None:
            output = ''
        else:
            parser = get_parser(data_type, gevent_safe=False)
            parser.initialize()
            parser.parse(content)
            output = render_to_string(
               self.templates_name % (DATA_TYPES[data_type]['name'],),
               {'node': parser.get_parsed(), 'attrs': flatatt(render_attrs),
                'input_type': attrs['id']})

        return output

