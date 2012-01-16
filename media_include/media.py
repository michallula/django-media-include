# -*- coding: utf-8 -*-
from django.forms.widgets import MEDIA_TYPES as django_media_types
from django.forms.widgets import Media as django_media
from django.utils.safestring import mark_safe
from itertools import chain

class Media(django_media):
    
    EXTRA_MEDIA_TYPES = ('script', 'stylesheet')
    
    MEDIA_TYPES = django_media_types + EXTRA_MEDIA_TYPES
    
    def __init__(self, media=None, **kwargs):
        if media:
            media_attrs = media.__dict__
        else:
            media_attrs = kwargs

        self._css = {}
        self._js = []
        self._script = []
        self._stylesheet = []

        for name in self.MEDIA_TYPES:
            getattr(self, 'add_' + name)(media_attrs.get(name, None))

    def __unicode__(self):
        return self.render()

    def render(self):
        return mark_safe(u'\n'.join(chain(*[getattr(self, 'render_' + name)() for name in self.MEDIA_TYPES])))
        
    def render_script(self):
        return self._script[:]
    
    def render_stylesheet(self):
        return self._stylesheet[:]

    def __getitem__(self, name):
        "Returns a Media object that only contains media of the given type"
        if name in self.MEDIA_TYPES:
            return self.__class__(**{str(name): getattr(self, '_' + name)})
        raise KeyError('Unknown media type "%s"' % name)
                        
    def add_stylesheet(self, data, *args, **kwargs):
        if data:
            for stylesheet in data:
                self._stylesheet.append(stylesheet)
    
    def add_script(self, data, *args, **kwargs):
        if data:
            for script in data:
                self._script.append(script)

    def __add__(self, other):
        combined = self.__class__()
        for name in self.MEDIA_TYPES:
            getattr(combined, 'add_' + name)(getattr(self, '_' + name, None))
            getattr(combined, 'add_' + name)(getattr(other, '_' + name, None))
        return combined
