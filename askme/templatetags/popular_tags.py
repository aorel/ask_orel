from django import template

from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('_inc_popular_tags.html')
def popular_tags():
    '''
    return {
        'test_popular_tags': [
            '_Test_tag1',
            '_Test_tag2',
            '_Test_tag3',
            '_Test_tag4',
            '_Test_tag5',
        ]
    }'''
    return {
        'test_popular_tags': cache.get('popular_tags'),
    }
