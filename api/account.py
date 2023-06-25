from django.contrib.auth import get_user_model
from django.test import TestCase


class AccountManagerTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="test", password="pass")
        self.assertEqual(user.username, "test")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(username="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", password="foo")
