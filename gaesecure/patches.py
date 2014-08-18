from copy import deepcopy
from functools import wraps
from logging import getLogger

from google.appengine.api import urlfetch

log = getLogger(__name__)

PATCHES_APPLIED = False


def override_default_kwargs(**overrides):
    """ Wraps a function to set different default values for some/all of the keyword arguments. """
    def decorator(function):
        @wraps(function)
        def replacement(*args, **kwargs):
            # Allow our default kwargs to be overriden if specified
            final_kwargs = deepcopy(overrides)
            final_kwargs.update(**kwargs)
            return function(*args, **final_kwargs)
        return replacement
    return decorator


def apply_patches():
    if PATCHES_APPLIED:
        log.info("apply_patches already called.  Ignoring.")

    # App Engine's urlfetch doesn't check SSL certificates by default.  WAT?  Fix that.
    urlfetch.fetch = override_default_kwargs(validate_certificate=True)(urlfetch.fetch)
    urlfetch.make_fetch_call = override_default_kwargs(validate_certificate=True)(urlfetch.make_fetch_call)
