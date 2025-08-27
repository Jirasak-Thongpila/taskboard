from django import template

register = template.Library()

@register.filter
def filter_completed(tasks):
    """Filter tasks that are completed"""
    return [task for task in tasks if task.done]

@register.filter
def filter_pending(tasks):
    """Filter tasks that are not completed"""
    return [task for task in tasks if not task.done]

@register.filter
def length(value):
    """Get length of a list"""
    return len(value)