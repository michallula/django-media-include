# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from django.template.loader import render_to_string
import re

__all__ = ('IncludeJSTestCase', 'IncludeCSSTestCase', 'IncludeMediaTestCase',
           'IncludeScriptTestCase', 'IncludeStylesheetTestCase')

class BaseTestCase(TestCase):
    
    template        = None
    result_template = None
    maxDiff = None
    
    def render(self, template=None, **kwargs):
        template=template or self.template
        return render_to_string(template, kwargs)
        
    def test(self):
        page = self.render()
        page = re.sub('\s', '', page)
        result = self.render(template=self.result_template)
        result = re.sub('\s', '', result)
        self.assertEqual(page, result)

class IncludeJSTestCase(BaseTestCase):
    
    template = 'media_include/tests/templatetags/include_js.html'
    result_template = 'media_include/tests/templatetags/include_js_result.html'
    
class IncludeCSSTestCase(BaseTestCase):
    
    template = 'media_include/tests/templatetags/include_css.html'
    result_template = 'media_include/tests/templatetags/include_css_result.html'
    
class IncludeMediaTestCase(BaseTestCase):
    
    template = 'media_include/tests/templatetags/include_media.html'
    result_template = 'media_include/tests/templatetags/include_media_result.html'
    
class IncludeScriptTestCase(BaseTestCase):
    
    template = 'media_include/tests/templatetags/include_script.html'
    result_template = 'media_include/tests/templatetags/include_script_result.html'
    
class IncludeStylesheetTestCase(BaseTestCase):
    
    template = 'media_include/tests/templatetags/include_stylesheet.html'
    result_template = 'media_include/tests/templatetags/include_stylesheet_result.html'
