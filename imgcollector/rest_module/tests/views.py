import tempfile

from django.test import TestCase, Client
from PIL import Image
from uuid import uuid4


class ViewsTestCase(TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.image_name:    str = "test image"
        self.username:      str = f"user_{uuid4().hex}"
        self.password:      str = uuid4().hex
        self.email:         str = f"{uuid4().hex}@mail.example"
        self.api_key:       str = ""
        self.refresh:       str = ""
        self.random_user:   dict = {}

    def test_users_without_auth(self) -> None:
        resp = Client().get("/users/")
        self.assertEqual(resp.status_code, 401)

    def _test_get_users(self, with_image: bool = False, random_user: bool = False) -> None:
        token = self.random_user["token"] if random_user else self.api_key
        self.assert_(token != "")

        # generate random user
        self._register_user(random_user=True)

        # try order all users
        resp_all_users = Client().get("/users/", HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(resp_all_users.status_code, 403)  # only superuser
        self.assertEqual(resp_all_users.json(), {
            "detail": "You do not have permission to perform this action."
        })

        # try order other user data
        resp_other_user = Client().get("/users/2/", HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(resp_other_user.status_code, 403)  # only superuser
        self.assertEqual(resp_other_user.json(), {
            "detail": "You do not have permission to perform this action."
        })

        # test user get
        resp_user_0 = Client().get("/users/1/", HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(resp_user_0.status_code, 200)
        self.assertEqual(resp_user_0.json(), {
            "id": 1,
            "username": self.username,
            "email": self.email,
            "is_active": True,
            "is_staff": False,
            "customer_type": "basic",
            "photos": resp_user_0.json()["photos"]
        })

    def test_images_without_auth(self) -> None:
        resp = Client().get("/images/")
        self.assertEqual(resp.status_code, 401)

    def _test_get_image_0(self) -> None:
        self.assert_(self.api_key != "")

        resp_image = Client().get("/images/1/", HTTP_AUTHORIZATION=f"Token {self.api_key}")
        self.assertEqual(resp_image.status_code, 200)
        self.assert_(resp_image.json()["image"] is None)
        self.assert_(resp_image.json()["creator"] == self.username)
        self.assert_(resp_image.json()["name"] == self.image_name)
        self.assert_(resp_image.json()["id"] == 1)

    def _test_images_upload(self, random_user: bool = False) -> None:
        token = self.random_user["token"] if random_user else self.api_key
        self.assert_(token != "")

        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(file)

        with open(file.name, 'rb') as data:
            resp = Client().post("/images/", {
                "name": self.image_name, "image": data},
                                 HTTP_AUTHORIZATION=f"Token {token}")
            self.assertEqual(resp.status_code, 201)
            self.assert_(resp.json()["image"] is None)
            self.assert_(resp.json()["creator"] == self.username)
            self.assert_(resp.json()["name"] == self.image_name)
            self.assert_(type(resp.json()["id"]) == int)

        self._test_get_users(with_image=True, random_user=random_user)

    def _test_get_images(self, random_user: bool = False) -> None:
        token = self.random_user["token"] if random_user else self.api_key
        self.assert_(token != "")

        resp = Client().get("/images/", HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })

        self._test_images_upload(random_user=random_user)

    def test_get_register(self) -> None:
        resp = Client().get("/register/")
        self.assertEqual(resp.status_code, 405)

    def _register_key(self, random_user: bool = True) -> None:
        resp_generate_key = Client().post("/api-token-auth/", {
            "username": self.username,
            "password": self.password
        })
        self.assertEqual(resp_generate_key.status_code, 200)
        self.assert_("token" in resp_generate_key.json().keys())

        token = resp_generate_key.json()["token"]
        if random_user:
            self.random_user["token"] = token
        else:
            self.api_key = token

        conf = {"random_user": random_user}
        self._test_get_users(**conf)
        self._test_get_images(**conf)

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

    def _register_user(self, random_user: bool = False) -> None:
        username = f"user_{uuid4().hex}" \
            if random_user else self.username
        password = uuid4().hex \
            if random_user else self.password
        email = f"{uuid4().hex}@mail.example" \
            if random_user else self.email

        resp_registered = Client().post("/register/", {
            "username": username,
            "password": password,
            "password2": password,
            "email": email
        })
        test_fields = ["username", "email", "first_name", "last_name"]
        self.assertEqual(resp_registered.status_code, 201)
        self.assert_(
            len([
                i for i in resp_registered.json().keys()
                if i in test_fields
            ]) == len(test_fields)
        )

        if random_user:
            self.random_user["username"] = username
            self.random_user["password"] = password
            self.random_user["email"] = email

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

        self._register_user()

        self._register_key()
        self._test_jwt_token()

        conf = {"random_user": True}
        self._register_user(**conf)
        self._register_key(**conf)

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
