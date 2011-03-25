"""A metaclass for slug prepopulation, to use together with transmeta.
"""

import copy

import django.forms.widgets
from django.conf import settings
import transmeta

class SlugMeta(django.forms.widgets.MediaDefiningClass):
    """A metaclass for slug prepopulation, to use together with
    transmeta.
    """
    def __new__(cls, name, bases, dct):
        new_dct = copy.copy(dct)

        if 'prepopulated_fields_translate' in dct:
            # First, we create the prepopulated fields entry
            if 'prepopulated_fields' not in dct:
                new_dct['prepopulated_fields'] = {}

            # Then, we loop through each of them, creating one prepopulated field per language
            for slug_field, other_fields in dct.get('prepopulated_fields_translate', {}).iteritems():
                for lang, _ in getattr(settings, 'LANGUAGES', ()):
                    new_dct['prepopulated_fields'][transmeta.get_real_fieldname(slug_field, lang)] = \
                        tuple([transmeta.get_real_fieldname(other_field, lang) for other_field in other_fields])

        return super(SlugMeta, cls).__new__(cls, name, bases, new_dct)
