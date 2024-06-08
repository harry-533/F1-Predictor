from django import template
from predictor.models import *

register = template.Library()

@register.simple_tag
def get_tracks():
    return Track.objects.all()

@register.simple_tag
def get_drivers():
    return Driver.objects.all()