# from django.contrib.auth import get_user_model
# from django.test import TestCase, Client
# from http import HTTPStatus
#
# User = get_user_model()
#
#
# class AboutUrlsTests(TestCase):
#     """Тесты для about.urls"""
#     def setUp(self):
#         self.guest_client = Client()
#         self.user = User.objects.create_user(username='author')
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)
#
#     def test_about_all_page_accessibility_test(self):
#         """Проверка доступности страниц для авторизованного пользователя."""
#         availability_url = [
#             'about/author/',
#             'about/tech/',
#         ]
#         for address in availability_url:
#             with self.subTest(address=address):
#                 response = self.authorized_client.get(address)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)
#
#     def test_about_urls_uses_correct_template(self):
#         """Проверка корректности вызываемых HTML-шаблонов."""
#         templates_url_names = {
#             '/about/author/': 'author.html',
#             '/about/tech/': 'tech.html',
#         }
#         for address, template in templates_url_names.items():
#             with self.subTest(address=address):
#                 response = self.authorized_client.get(address)
#                 self.assertTemplateUsed(response, template)
