# -*- coding: utf-8 -*-

from django import template
from media_include.settings import MEDIA_CLASS, MEDIA_CONTEXT_KEY
from django.utils.encoding import smart_str
from media_include.media import Media

register = template.Library()

#===============================================================================
# helpers
#===============================================================================

MEDIA_CLASS = Media

def parse(parser, *bits):
    args = []
    kwargs = {}
    for bit in bits:
        splited = bit.split("=", 1)
        if len(splited) > 1:
            key = smart_str(splited[0], encoding='asci', strings_only=True)
            val = parser.compile_filter(splited[1])
            kwargs[key] = val
        else:
            args.append(parser.compile_filter(bit))
    return args, kwargs

class MediaContext(object):
    
    media_class = MEDIA_CLASS
    
    def __init__(self):
        self.media = self.media_class()

    def add(self, media):
        self.media += media

class BaseNode(template.Node):
    
    tag_name            = None
    media_class         = MEDIA_CLASS
    media_context_key   = MEDIA_CONTEXT_KEY
    
    @classmethod
    def parse(cls, parser, token):
        bits = token.split_contents()
        assert bits[0] == cls.tag_name
        args, kwargs = parse(parser, *bits[1:])
        return cls(parser, *args, **kwargs)
    
    def __init__(self, parser, *args, **kwargs):
        self.parser     = parser
        self.args       = args
        self.kwargs     = kwargs
        
    def resolve(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = {}
        for key, val in self.kwargs.iteritems():
            kwargs[key] = val.resolve(context)
        return args, kwargs
    
    def get_media_context(self, context):
        if self.media_context_key not in context.render_context:
            context.render_context[self.media_context_key] = MediaContext()
        return context.render_context[self.media_context_key]
        
    def get_media(self, context):
        return self.media_class()

#===============================================================================
# injection nodes
#===============================================================================

class InjectMediaNode(BaseNode):
    
    tag_name = u'inject_media'
    
    def get_media(self, context):
        return self.get_media_context(context).media
    
    def render(self, context):
        return self.get_media(context)
    
class InjectJSNode(InjectMediaNode):
    
    tag_name = u'inject_js'
    
    def render(self, context):
        return super(InjectJSNode, self).render(context).render_js()

class InjectCSSNode(InjectMediaNode):
    
    tag_name = u'inject_css'
    
    def render(self, context):
        return super(InjectCSSNode, self).render(context).render_css()
    
class InjectScriptNode(InjectMediaNode):
    
    tag_name = u'inject_script'
    
    def render(self, context):
        return super(InjectScriptNode, self).render(context).render_script()
    
class InjectStylesheetNode(InjectMediaNode):
    
    tag_name = u'inject_stylesheet'
    
    def render(self, context):
        return super(InjectStylesheetNode, self).render(context).render_stylsheet()

#===============================================================================
# inclusion nodes
#===============================================================================

class BaseIncludeNode(BaseNode):
    
    def render(self, context):
        media = self.get_media(context)
        media_context = self.get_media_context(context)
        media_context.add(media)
        return ''

class IncludeJSNode(BaseIncludeNode):
    
    tag_name = u'include_js'
    
    def get_media(self, context):
        media = super(IncludeJSNode, self).get_media(context)
        args, _ = self.resolve(context)
        media.add_js(args)
        return media

class IncludeCSSNode(BaseIncludeNode):
    
    def get_media(self, context):
        media = super(IncludeCSSNode, self).get_media(context)
        args, kwargs = self.resolve(context)
        if args and 'all' not in kwargs:
            kwargs['all'] = args
        media.add_css(kwargs)
        return media
    
    tag_name = u'include_css'

class IncludeMediaNode(BaseIncludeNode):
    
    tag_name = u'include_media'
    
class ComplexIncludeNode(BaseIncludeNode):
    
    tag_name = None
    end_tag_name = None
    
    @classmethod
    def parse(cls, parser, token):        
        bits = token.split_contents()
        assert bits[0] == cls.tag_name
        args, kwargs = parse(parser, *bits[1:])
        nodelist = parser.parse(cls.end_tag_name)
        parser.delete_first_token()
        return cls(parser, nodelist, *args, **kwargs) 
    
    def __init__(self, parser, nodelist, *args, **kwargs):
        self.nodelist = nodelist
        super(ComplexIncludeNode, self).__init__(parser, *args, **kwargs)
    
class IncludeScriptNode(ComplexIncludeNode):
    
    tag_name = u'include_script'    
    end_tag_name = u'end{0}'.format(tag_name)
    
    def get_media(self, context):
        media = super(IncludeScriptNode, self).get_media(context)
        script = self.nodelist.render(context)
        media.add_script([script])
        return media

class IncludeStylesheetNode(ComplexIncludeNode):
    
    tag_name = u'include_stylesheet'
    end_tag_name = u'end{0}'.format(tag_name)
    
    def get_media(self, context):
        media = super(IncludeStylesheetNode, self).get_media(context)
        stylesheet = self.nodelist.render(context)
        media.add_stylesheet([stylesheet])
        return media

#===============================================================================
# media include node
#===============================================================================
    
class MediaIncludeNode(template.Node):
    
    tag_name        = u'media_include'
    end_tag_name    = u'end{0}'.format(tag_name)
    
    @classmethod
    def parse(cls, parser, token):        
        bits = token.split_contents()
        assert bits[0] == cls.tag_name
        args, kwargs = parse(parser, *bits[1:])
        nodelist = parser.parse(cls.end_tag_name)
        parser.delete_first_token()
        return cls(parser, nodelist, *args, **kwargs)
    
    def __init__(self, parser, nodelist, *args, **kwargs):
        self.nodelist = nodelist
        
    def render(self, context):
        injections, bits = [], []
        context.push()
        for node in self.nodelist:
            if isinstance(node, InjectMediaNode):
                injections.append((node, bits))
                bits = []
            else:
                bits.append(unicode(node.render(context)))
        injections.append((None, bits))
        result = []        
        for injection, bits  in injections:
            result.extend(bits)
            if injection:
                result.append(unicode(injection.render(context)))
        return u''.join(result)

#===============================================================================
# tags registration
#===============================================================================

for cls in (MediaIncludeNode, 
            InjectMediaNode, InjectJSNode, InjectCSSNode, InjectScriptNode, 
            InjectStylesheetNode, 
            IncludeMediaNode, IncludeJSNode, IncludeCSSNode, IncludeScriptNode, 
            IncludeStylesheetNode):
    register.tag(cls.tag_name, cls.parse)
