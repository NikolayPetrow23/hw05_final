from http import HTTPStatus

from .fixtures import const as con
from .fixtures.fixtures_data_and_user import PostsTests


class PostsUrlsTests(PostsTests):
    """Тесты для posts.urls"""
    def test_all_page_accessibility_authorized_user(self):
        """
        Проверяем, доступность страниц
        для авторизованного пользователя.
        """
        for address in self.address_page_url:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_all_page_accessibility_unauthorized_user(self):
        """
        Проверяем, доступность страниц
        для авторизованного пользователя.
        """
        for address in self.address_page_unauthorized_user:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_non_existent_page_404(self):
        """Проверка ошибки 404."""
        response = self.authorized_client.get(con.UNEXISTING)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, con.TEMPLATE_404)

    def test_post_list_url_redirect_anonymous_on_admin_login(self):
        """
        Проверяем, корректность редиректов для
        неавторизованного пользователя.
        """
        redirect_url = {
            '/auth/login/?next=/create/': (
                self.address_page_url[con.INDEX_NUMBER_POST_CREATE]),
            f'/auth/login/?next=/posts/{self.post.pk}/edit/': (
                self.address_page_url[con.INDEX_NUMBER_POST_EDIT]),
        }
        for login, address in redirect_url.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertRedirects(response, login)

    def test_posts_urls_uses_correct_template(self):
        """Проверяем, корректность вызываемых HTML-шаблонов."""
        templates_url_names = dict(zip(self.address_page_url,
                                       self.templates_names))
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
