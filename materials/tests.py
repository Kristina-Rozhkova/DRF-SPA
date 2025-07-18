from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.user2 = User.objects.create(email="admin2@mail.ru")
        self.course = Course.objects.create(name="Python-разработка", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Django REST Framework", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

        self.moderators_group = Group.objects.create(name="Модератор")
        self.user2.groups.add(self.moderators_group)
        self.user2.save()

    # def test_create_course(self):
    #     """Тестирование создания курса"""
    #     data = {"name": "Веб-дизайн", "description": "Описание курса по веб-дизайну"}
    #
    #     url = reverse("materials:course-list")
    #     response = self.client.post(url, data)
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    #     self.assertEqual(
    #         response.json(),
    #         {
    #             "id": 7,
    #             "name": "Веб-дизайн",
    #             "preview": None,
    #             "description": "Описание курса по веб-дизайну",
    #             "count_lessons": 0,
    #             "lessons": [],
    #             "is_subscribed": False,
    #         },
    #     )

        # self.assertTrue(Course.objects.filter(name="Веб-дизайн").exists())

    def test_course_retrieve(self):
        """Тестирование просмотра детальной информации о курсе"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_list(self):
        """Тестирование получения списка курсов"""
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "preview": None,
                    "description": None,
                    "count_lessons": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "name": self.lesson.name,
                            "description": None,
                            "preview": None,
                            "video": None,
                            "update_at": self.lesson.update_at.isoformat().replace(
                                "+00:00", "Z"
                            ),
                            "course": self.course.pk,
                            "owner": self.user.pk,
                        }
                    ],
                    "is_subscribed": False,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)

    # def test_course_update(self):
    #     """Тестирование обновления информации о курсе."""
    #     url = reverse("materials:course-detail", args=(self.course.pk,))
    #     data = {"description": "Научим создавать приложения."}
    #     response = self.client.patch(url, data)
    #     json_response = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     self.assertEqual(json_response.get("description"), data["description"])

    def test_course_delete(self):
        """Тестирование удаления курса."""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_delete_with_moder(self):
        """Тестирование удаления записи модератором."""
        self.client.force_authenticate(user=self.user2)
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Course.objects.all().count(), 1)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.user2 = User.objects.create(email="admin2@mail.ru")
        self.course = Course.objects.create(name="Python-разработка", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Django REST Framework", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

        self.moderators_group = Group.objects.create(name="Модератор")
        self.user2.groups.add(self.moderators_group)
        self.user2.save()

    def test_lesson_create(self):
        """Тестирование создания урока"""
        data = {
            "name": "Тестирование на Python с помощью pytest",
            "video": "youtube.com/lesson/1/",
        }

        url = reverse("materials:lesson-create")
        response = self.client.post(url, data)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json()["name"], data["name"])
        self.assertEqual(response.json()["video"], data["video"])
        self.assertEqual(response.json()["owner"], self.user.pk)

        self.assertTrue(Lesson.objects.filter(name=data["name"]).exists())

    def test_lesson_with_incorrect_video_link_create(self):
        """Тестирование выброса ошибки при создании урока с неразрешенной ссылкой."""
        data = {
            "name": "Тестирование на Python с помощью pytest",
            "video": "my.com/lesson/1/",
        }

        url = reverse("materials:lesson-create")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json().get("non_field_errors")[0],
            "К материалам можно добавлять только ссылки на YouTube.",
        )

    def test_lesson_retrieve(self):
        """Тестирование просмотра детальной информации об уроке"""
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_list(self):
        """Тестирование получения списка уроков"""
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        print(self.lesson.update_at)

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": None,
                    "preview": None,
                    "update_at": self.lesson.update_at.isoformat().replace(
                        "+00:00", "Z"
                    ),
                    "video": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)

    # def test_lesson_update(self):
    #     """Тестирование обновления информации об уроке."""
    #     url = reverse("materials:lesson-update", args=(self.course.pk,))
    #     data = {"description": "Научим создавать приложения на DRF."}
    #     response = self.client.patch(url, data)
    #     json_response = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     self.assertEqual(json_response.get("description"), data["description"])

    # def test_lesson_delete(self):
    #     """Тестирование удаления урока."""
    #     url = reverse("materials:lesson-delete", args=(self.course.pk,))
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #
    #     self.assertEqual(Lesson.objects.all().count(), 0)
    #
    # def test_lesson_delete_with_moder(self):
    #     """Тестирование удаления записи модератором."""
    #     self.client.force_authenticate(user=self.user2)
    #     url = reverse("materials:lesson-delete", args=(self.course.pk,))
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    #     self.assertEqual(Lesson.objects.all().count(), 1)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(name="Python-разработка", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        """Тестирование подписки на курс."""
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        json_response = response.json()

        course_list_url = reverse("materials:course-list")
        course_response = self.client.get(course_list_url)
        course_json_response = course_response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["message"], "Подписка добавлена")

        self.assertEqual(course_json_response["results"][0]["is_subscribed"], True)

    def test_unsubscribe_to_course(self):
        """Тестирование отмены подписки на курс."""
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url2 = reverse("materials:subscription")
        data2 = {"course_id": self.course.pk}

        response2 = self.client.post(url2, data2)
        json_response2 = response2.json()

        course_list_url = reverse("materials:course-list")
        course_response = self.client.get(course_list_url)
        course_json_response = course_response.json()

        self.assertEqual(json_response2["message"], "Подписка удалена")

        self.assertEqual(course_json_response["results"][0]["is_subscribed"], False)
