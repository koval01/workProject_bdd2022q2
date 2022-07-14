from django.test import TestCase, Client
from uuid import uuid4


class ViewsTestCase(TestCase):
    def __init__(self) -> None:
        super().__init__()

        self.username = f"user_{uuid4().hex}"
        self.password = uuid4().hex
        self.email = f"{uuid4().hex}@mail.example"

    def test_users_without_auth(self) -> None:
        resp = Client().get("/users/")
        self.assertEqual(resp.status_code, 401)

    def test_images_without_auth(self) -> None:
        resp = Client().get("/images/")
        self.assertEqual(resp.status_code, 401)

    def test_get_register(self) -> None:
        resp = Client().get("/register/")
        self.assertEqual(resp.status_code, 405)

    def test_post_register(self) -> None:
        resp_null = Client().post("/register/")
        self.assertEqual(resp_null.status_code, 400)
        self.assertEqual(resp_null.json(), {
            "username": ["This field is required."],
            "password": ["This field is required."],
            "password2": ["This field is required."],
            "email": ["This field is required."]
        })
        resp_no_password2 = Client().post("/register/", {
            "username": self.username,
            "password": self.password,
            "password2": "",
            "email": self.email
        })
        self.assertEqual(resp_no_password2.status_code, 400)
        self.assertEqual(resp_no_password2.json(), {
            "password2": ["This field may not be blank."]
        })

    def test_get_api_token_auth(self) -> None:
        resp = Client().get("/api-token-auth/")
        self.assertEqual(resp.status_code, 405)

    def test_post_api_token_auth(self) -> None:
        resp_null = Client().post("/api-token-auth/")
        self.assertEqual(resp_null.status_code, 400)
        self.assertEqual(resp_null.json(), {
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
