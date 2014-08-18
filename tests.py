from django.http import HttpRequest, HttpResponse
from django.test import TestCase
import mock

from gaesecure.decorators import task_queue_only, cron_only, gae_admin_only
from gaesecure.patches import override_default_kwargs


class DecoratorsTest(TestCase):

    def test_task_queue_only(self):
        """ Test the `task_queue_only` decorator. """
        @task_queue_only
        def my_view(request):
            return HttpResponse("OK")

        standard_request = HttpRequest()
        task_request = HttpRequest()
        task_request.META['X_APPENGINE_QUEUENAME'] = "my-queue"

        standard_response = my_view(standard_request)
        task_response = my_view(task_request)

        self.assertEqual(standard_response.status_code, 403)
        self.assertNotEqual(standard_response.content, "OK")
        self.assertEqual(task_response.status_code, 200)
        self.assertEqual(task_response.content, "OK")


    def test_cron_only(self):
        """ Test the `cron_only` decorator. """
        @cron_only
        def my_view(request):
            return HttpResponse("OK")

        standard_request = HttpRequest()
        cron_request = HttpRequest()
        cron_request.META['X_APPENGINE_CRON'] = "my-queue"

        standard_response = my_view(standard_request)
        cron_response = my_view(cron_request)

        self.assertEqual(standard_response.status_code, 403)
        self.assertNotEqual(standard_response.content, "OK")
        self.assertEqual(cron_response.status_code, 200)
        self.assertEqual(cron_response.content, "OK")

    def test_gae_admin_only(self):
        """ Test the `gae_admin_only` decorator. """
        @gae_admin_only
        def my_view(request):
            return HttpResponse("OK")

        with mock.patch("gaesecure.decorators.is_current_user_admin", True):
            response = my_view(HttpRequest())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, "OK")

        with mock.patch("gaesecure.decorators.is_current_user_admin", False):
            response = my_view(HttpRequest())
            self.assertEqual(response.status_code, 403)
            self.assertNotEqual(response.content, "OK")


def PatchesTest(TestCase):

    # This is a decorator too, really.
    def test_override_default_kwargs(self):
        """ Test the `override_default_kwargs` decorator. """

        @override_default_kwargs(c=7)
        def my_func(a, b=1, c=2):
            return ",".join([a,b,c])

        # Test that the default override works
        self.assertEqual(my_func(0), "0,1,7")
        # Test that we can still specify our own values for all kwargs if we want to
        self.assertEqual(my_func(0, b=3, c=5), "0,3,5")
