import dateutil.parser
import httplib2

try:
    import json
except ImportError:
    import simplejson as json

from django.conf import settings
from django.utils.encoding import smart_unicode, force_unicode


DEFAULT_HTTP_HEADERS = {
    "User-Agent" : getattr(settings, "USER_AGENT", "chrisamico.com")
}


def getjson(url, **kwargs):
    """Fetch and parse some JSON. Returns the deserialized JSON."""
    response = fetch_resource(url, **kwargs)
    return json.loads(response)


def fetch_resource(url, method="GET", body=None, username=None, password=None, headers=None):
    h = httplib2.Http(timeout=15)
    h.force_exception_to_status_code = True
    
    if username is not None or password is not None:
        h.add_credentials(username, password)
    
    if headers is None:
        headers = DEFAULT_HTTP_HEADERS.copy()
    
    response, content = h.request(url, method, body, headers)
    return content


def parsedate(s):
    """
    Convert a string into a (local, naive) datetime object.
    """
    dt = dateutil.parser.parse(s)
    if dt.tzinfo:
        dt = dt.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)
    return dt


def safeint(s):
    """Always returns an int. Returns 0 on failure."""
    try:
        return int(force_unicode(s))
    except (ValueError, TypeError):
        return 0
