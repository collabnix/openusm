'''
Created on Jun 22, 2017

@author: Avinash_Bendigeri
'''

from django import template

register = template.Library()


@register.filter
def hash(h, key):
    print key
    return h[key]