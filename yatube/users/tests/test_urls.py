# from http import HTTPStatus
#
# from yatube.users.tests.fixtures.fixtures_user import UsersTests
# from .fixtures import const as con
#
#
# class UserUrlsTests(UsersTests):
#     """Тесты для user.urls"""
#     def test_user_anonymous_user_access(self):
#         """
#         Проверка доступности страниц для неавторизованного пользователя.
#         """
#         for address in self.address_page_unauthorized_users:
#             with self.subTest(address=address):
#                 response = self.guest_client.get(address)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)
#
#     def test_user_access_for_an_authorized_user(self):
#         """Проверка доступности страниц для авторизованного пользователя."""
#         for address in self.address_page_authorized_user:
#             with self.subTest(address=address):
#                 response = self.authorized_client.get(address)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)
#
#     def test_user_list_url_redirect_anonymous_on_admin_login(self):
#         """Проверка редиректов для неавторизованного пользователя."""
#         anonymous_redirect_url = dict(zip(
#             self.addresses_page_redirects,
#             self.redirects_page_unauthorized_user
#         ))
#         for login, address in anonymous_redirect_url.items():
#             with self.subTest(address=address):
#                 response = self.guest_client.get(address, follow=True)
#                 self.assertRedirects(response, login)
#
#     def test_user_list_url_redirect_authorized_on_admin_login(self):
#         """Проверка редиректов для авторизованного пользователя."""
#         authorized_redirect_url = dict(zip(
#             self.address_page_authorized_user[con.INDEX_USER_CHANGE],
#             self.address_page_authorized_user[con.INDEX_USER_CHANGE_DONE])
#         )
#         for login, address in authorized_redirect_url.items():
#             with self.subTest(address=address):
#                 response = self.authorized_client.get(address, follow=True)
#                 self.assertRedirects(response, login)
#
#     def test_user_anonymous_urls_uses_correct_template(self):
#         """
#         Проверка корректности вызываемых HTML-шаблонов
#         для неавторизованного пользователя.
#         """
#         templates_url_names = dict(zip(self.address_page_unauthorized_users,
#                                        self.template_names_unauthorized_users))
#         for address, template in templates_url_names.items():
#             with self.subTest(address=address):
#                 response = self.guest_client.get(address)
#                 self.assertTemplateUsed(response, template)
#
#     def test_user_authorized_urls_uses_correct_template(self):
#         """
#         Проверка корректности вызываемых HTML-шаблонов
#         для авторизованного пользователя.
#         """
#         templates_url_names = dict(zip(self.address_page_authorized_user,
#                                        self.template_names_authorized_users))
#         for address, template in templates_url_names.items():
#             with self.subTest(address=address):
#                 response = self.authorized_client.get(address)
#                 self.assertTemplateUsed(response, template)
