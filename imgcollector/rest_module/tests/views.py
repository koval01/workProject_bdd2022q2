from django.test import TestCase


class PollsViewsTestCase(TestCase):

    def test_users_without_auth(self):
        resp = self.client.get("users")
        self.assertEqual(resp.status_code, 401)
