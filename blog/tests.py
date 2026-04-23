from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Post, Comment
from .views import post_list
from unittest.mock import patch


# --- 1. Тестування Моделей (Бази даних) - Покриття 100% ---
class ModelTests(TestCase):
    def setUp(self):
        # Ця функція запускається ПЕРЕД кожним тестом. Створюємо фейкового юзера і пост.
        self.user = User.objects.create_user(username='testuser', password='password123') 
        self.post = Post.objects.create(title='Тестовий пост', content='Текст', author=self.user)

    def test_post_model_str(self):
        # Перевіряємо, чи правильно працює метод __str__ у моделі Post
        self.assertEqual(str(self.post), 'Тестовий пост')

    def test_comment_model_str(self):
        # Створюємо коментар і перевіряємо його текстове відображення
        comment = Comment.objects.create(post=self.post, author=self.user, text='Супер!')
        expected_str = f"Коментар від {self.user} до поста {self.post}"
        self.assertEqual(str(comment), expected_str)


# --- 2. Тестування Контролера (Views) із використанням Mock ---
class ViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # Використовуємо patch (Mock), щоб підмінити звернення до бази даних!
    @patch('blog.views.Post.objects.all')
    def test_post_list_view_mock(self, mock_post_all):
        # Налаштовуємо Mock: коли view спробує дістати пости, ми повернемо порожній список
        # без реального звернення до бази даних.
        mock_post_all.return_value.order_by.return_value = []

        # Створюємо фейковий запит на головну сторінку
        request = self.factory.get('/')

        # Викликаємо нашу функцію-контролер
        response = post_list(request)

        # Перевіряємо, що сторінка завантажилась успішно (код 200)
        self.assertEqual(response.status_code, 200)

        # Перевіряємо, що наш Mock (підроблена база даних) був викликаний 1 раз
        mock_post_all.assert_called_once()