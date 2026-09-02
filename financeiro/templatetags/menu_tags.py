from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active_menu(context, *keywords):
    request = context.get('request')
    if not request:
        return ''
    
    resolver = getattr(request, 'resolver_match', None)
    if resolver and getattr(resolver, 'url_name', None):
        url_name = resolver.url_name
        for kw in keywords:
            if kw == url_name:
                return 'active'

    path = request.path.strip('/')
    segments = path.split('/') if path else []
    for kw in keywords:
        if kw in segments:
            return 'active'

    return ''
