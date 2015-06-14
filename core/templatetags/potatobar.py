import re
from google.appengine.api import urlfetch, memcache

from django import template
register = template.Library()


POTATOBAR_URL = "https://p.ota.to/static/potatobar.html"
POTATOBAR_MC_KEY = "potatobar"


@register.simple_tag
def potatobar():

    potatobar = memcache.get(POTATOBAR_MC_KEY)

    if potatobar is not None:
        return potatobar
    else:
        result = urlfetch.fetch(POTATOBAR_URL)

        if result.status_code == 200:
            potatobar = result.content

            cache_header = result.headers.get("cache-control", None)
            if cache_header:
                cache_regex = re.match(r"^(.*)max-age=(?P<cache_time>\d+)(.*)$", cache_header)
                cache_time = int(cache_regex.groupdict().get("cache_time", 0))

            memcache.add(POTATOBAR_MC_KEY, potatobar, cache_time)
            return potatobar
        else:
            return ""