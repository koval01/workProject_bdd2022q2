from django.test import TestCase, Client


class PollsViewsTestCase(TestCase):

    def test_users_without_auth(self):
        resp = Client().get("/users/")
        self.assertEqual(resp.status_code, 401)

    def test_images_without_auth(self):
        resp = Client().get("/images/")
        self.assertEqual(resp.status_code, 401)

    def test_get_api_token_auth(self):
        resp = Client().get("/api-token-auth/")
        self.assertEqual(resp.status_code, 405)

    def test_post_api_token_auth(self):
        resp_unknown_user = Client().post("/api-token-auth/")
        self.assertEqual(resp_unknown_user.status_code, 400)
        self.assertEqual(resp_unknown_user.json(), {
            "username": ["This field is required."],
            "password": ["This field is required."]
        })
        resp_unknown_user = Client().post("/api-token-auth/", {
            "username": "none",
            "password": "none"
        })
        self.assertEqual(resp_unknown_user.status_code, 400)
        self.assertEqual(resp_unknown_user.json(), {
            "non_field_errors": ["Unable to log in with provided credentials."]
        })
