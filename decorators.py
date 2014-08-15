from functools import wraps

from django.http import HttpResponseForbidden
from google.appengine.api.users import current_user_is_admin


def task_queue_only(view_func):
    """ View decorator that only allows requests which originate from the App Engine task queue.
    """
    @wraps(view_func)
    def new_view(request, *args, **kwargs):
        if not request.META.get("X_APPENGINE_QUEUENAME"):
            return HttpResponseForbidden("Task queue requests only.")
        return view_func(request, *args, **kwargs)


def cron_only(view_func):
    """ View decorator that only allows requests which originate from an App Engine cron.
    """
    @wraps(view_func)
    def new_view(request, *args, **kwargs):
        if not request.META.get("X_APPENGINE_CRON"):
            return HttpResponseForbidden("Cron requests only.")
        return view_func(request, *args, **kwargs)


def gae_admin_only(view_func):
    """ View decorator that requires the user to be an administrator of the App Engine app. """
    @wraps(view_func)
    def new_view(*args, **kwargs):
        if not current_user_is_admin():
            return HttpResponseForbidden("Cron requests only.")
        return view_func(*args, **kwargs)

