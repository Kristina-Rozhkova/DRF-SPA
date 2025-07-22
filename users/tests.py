from unittest.mock import patch, MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """Тестирование создания пользователя."""
        data = {"email": "stanislav@list.ru", "password": "111111"}

        url = reverse("users:user-create")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.all().count(), 2)

    def test_user_token(self):
        """Тестирование получения токена для пользователя."""
        self.user.set_password("123")
        self.user.save()
        data = {"email": self.user.email, "password": "123"}

        token_url = reverse("users:token_obtain_pair")
        response = self.client.post(token_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_token_refresh(self):
        """Тестирование обновления токена для пользователя."""
        self.user.set_password("123")
        self.user.save()
        data = {"email": self.user.email, "password": "123"}

        token_url = reverse("users:token_obtain_pair")
        token_response = self.client.post(token_url, data)
        refresh_token = token_response.json()["refresh"]

        refresh_data = {"refresh": refresh_token}

        refresh_token_url = reverse("users:token_refresh")
        response = self.client.post(refresh_token_url, refresh_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list(self):
        """Тестирование просмотра списка пользователей."""
        url = reverse("users:user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            [
                {
                    "email": self.user.email,
                    "first_name": "",
                    "city": None,
                    "avatar": None,
                }
            ],
        )

    def test_user_detail(self):
        """Тестирование просмотра профиля пользователя."""
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "email": self.user.email,
                "first_name": "",
                "last_name": "",
                "phone": None,
                "city": None,
                "avatar": None,
                "payment": [],
            },
        )

    def test_another_user_detail(self):
        """Тестирование просмотра профиля пользователя другим пользователем."""
        data = {"email": "stanislav@list.ru", "password": "111111"}

        url = reverse("users:user-create")
        post_response = self.client.post(url, data)
        user_pk = post_response.json().get("id")

        url_detail = reverse("users:user-detail", args=(user_pk,))
        response = self.client.get(url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "email": "stanislav@list.ru",
                "first_name": "",
                "city": None,
                "avatar": None,
            },
        )

    def test_user_update(self):
        """Тестирование обновления профиля"""
        data = {"city": "Москва"}

        url = reverse("users:user-update", args=(self.user.pk,))
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "email": "admin@mail.ru",
                "first_name": "",
                "last_name": "",
                "phone": None,
                "city": "Москва",
                "avatar": None,
                "payment": [],
            },
        )

    def test_user_delete(self):
        """Тестирование удаления пользователя."""
        url = reverse("users:user-delete", args=(self.user.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(User.objects.all().count(), 0)


class PayTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(name="Python-разработка")
        self.client.force_authenticate(user=self.user)

    @patch('users.services.stripe.Price.create')
    @patch('users.services.stripe.checkout.Session.create')
    def test_create_payment(self, mock_session_create, mock_price_create):
        """Тестирование добавления оплаты курсов."""
        mock_price = MagicMock()
        mock_price.id = 'price_test123'
        mock_price_create.return_value = mock_price

        mock_session_create.return_value = {
            'id': 'sess_test123',
            'url': 'https://checkout.stripe.com/pay/test'
        }

        data = {
            "course": self.course.pk,
            "amount": 150000,
            "form_of_payment": "Наличные",
            "payment_status": "unpaid",
            "user": self.user.pk,
        }
        url = reverse("users:pay-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["amount"], data["amount"])
        self.assertEqual(response.json()["form_of_payment"], data["form_of_payment"])
        self.assertEqual(response.json()["payment_status"], data["payment_status"])
        self.assertEqual(response.json()["user"], self.user.pk)
        self.assertEqual(response.json()["course"], self.course.pk)
        self.assertEqual(response.json()["lesson"], None)

        mock_price_create.assert_called_once()
        mock_session_create.assert_called_once()

