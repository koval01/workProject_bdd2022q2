from django.test import TestCase, Client
from uuid import uuid4


class ViewsTestCase(TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.username = f"user_{uuid4().hex}"
        self.password = uuid4().hex
        self.email = f"{uuid4().hex}@mail.example"
        self.api_key = ""
        self.refresh = ""

    def test_users_without_auth(self) -> None:
        resp = Client().get("/users/")
        self.assertEqual(resp.status_code, 401)

    def _test_get_users(self) -> None:
        self.assert_(self.api_key != "")

        resp = Client().get("/users/", HTTP_AUTHORIZATION=f"Token {self.api_key}")
        self.assertEqual(resp.status_code, 403)  # only superuser
        self.assertEqual(resp.json(), {
            "detail": "You do not have permission to perform this action."
        })

        # test user get
        resp_user_0 = Client().get("/users/1/", HTTP_AUTHORIZATION=f"Token {self.api_key}")
        self.assertEqual(resp_user_0.status_code, 200)
        self.assertEqual(resp_user_0.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "username": self.username,
                    "email": self.email,
                    "is_active": True,
                    "is_staff": False,
                    "customer_type": "basic",
                    "photos": []
                }
            ]
        })

    def test_images_without_auth(self) -> None:
        resp = Client().get("/images/")
        self.assertEqual(resp.status_code, 401)

    def _test_get_images(self) -> None:
        self.assert_(self.api_key != "")

        resp = Client().get("/images/", HTTP_AUTHORIZATION=f"Token {self.api_key}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })

    def test_get_register(self) -> None:
        resp = Client().get("/register/")
        self.assertEqual(resp.status_code, 405)

    def _register_key(self) -> None:
        resp_generate_key = Client().post("/api-token-auth/", {
            "username": self.username,
            "password": self.password
        })
        self.assertEqual(resp_generate_key.status_code, 200)
        self.assert_("token" in resp_generate_key.json().keys())
        self.api_key = resp_generate_key.json()["token"]

        self._test_get_images()
        self._test_get_users()

    def _test_refresh_jwt(self) -> None:
        self.assert_(self.refresh != "")

        resp = Client().post("/token/refresh/", {
            "username": self.username,
            "password": self.password,
            "refresh": self.refresh
        })
        self.assertEqual(resp.status_code, 200)
        self.assert_("access" in resp.json().keys())

    def _test_jwt_token(self) -> None:
        resp = Client().post("/token/", {
            "username": self.username,
            "password": self.password
        })
        test_fields = ["refresh", "access"]
        self.assertEqual(resp.status_code, 200)
        self.assert_(len([
            i for i in resp.json().keys()
            if i in test_fields
        ]) == len(test_fields))
        self.refresh = resp.json()["refresh"]

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

        resp_registered = Client().post("/register/", {
            "username": self.username,
            "password": self.password,
            "password2": self.password,
            "email": self.email
        })
        test_fields = ["username", "email", "first_name", "last_name"]
        self.assertEqual(resp_registered.status_code, 201)
        self.assert_(
            len([
                i for i in resp_registered.json().keys()
                if i in test_fields
            ]) == len(test_fields)
        )

        self._register_key()
        self._test_jwt_token()

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
