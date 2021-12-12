from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, value):
    request = context['request'].GET.copy()
    request['ordering'] = value
    return request.urlencode()
