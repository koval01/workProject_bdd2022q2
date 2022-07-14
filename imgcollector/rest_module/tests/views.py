from django.test import TestCase, Client


class PollsViewsTestCase(TestCase):

    def test_users_without_auth(self):
        resp = Client().get("/users/")
        self.assertEqual(resp.status_code, 401)
