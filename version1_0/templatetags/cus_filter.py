from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def listGetter(_list, index):
    # dictitionary is a Python dict,
    # and key is a django.utils.safestring.SafeType object
    index = int(index)
    if not (len(_list) > index >= 0):
        return None
    value = _list[index]
    return value


def getType(value):
    # dictitionary is a Python dict,
    # and key is a django.utils.safestring.SafeType object
    return type(value)


register.filter(name='listGetter', filter_func=listGetter, is_safe=True)
register.filter(name='getType', filter_func=getType, is_safe=True)
