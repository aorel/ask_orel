from django import template

from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('_inc_best_members.html')
def best_members():
    '''
    return {
        'test_best_members': [
            '_Test_member1',
            '_Test_member2',
            '_Test_member3',
            '_Test_member4',
            '_Test_member5',
        ]
    }'''
    return {
        'test_best_members': cache.get('best_members'),
    }
