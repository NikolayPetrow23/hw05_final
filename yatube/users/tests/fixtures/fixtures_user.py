from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from . import const as con

User = get_user_model()


class UsersTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=con.USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.test_uidb64 = 'OA'
        self.test_token = '67p-7e697ad27d9ad77d97e2'
        self.form_data = {
            'first_name': 'Nikolay',
            'last_name': 'Petrov',
            'username': 'nikola23',
            'email': 'nikola23@gmail.com',
            'password1': 'nikolay123',
            'password2': 'nikolay123',
        }

        # Списов namespace:name страниц users.
        self.page_namespace_and_name = [
            reverse('users:signup'),
            reverse('users:logout'),
            reverse('users:login'),
            reverse('users:password_reset_form'),
            reverse('users:password_reset_done'),
            reverse('users:password_reset_confirm',
                    kwargs={
                        'uidb64': self.test_uidb64,
                        'token': self.test_token
                    }),
            reverse('users:password_reset_complete'),
            reverse('users:password_change'),
            reverse('users:password_change_done'),
        ]

        # Список HTML-шаблонов для не авторизованного пользователя.
        self.template_names_unauthorized_users = [
            con.TEMPLATE_AUTH_SIGNUP,
            con.TEMPLATE_AUTH_LOGOUT,
            con.TEMPLATE_AUTH_LOGIN,
            con.TEMPLATE_AUTH_PASSWORD_RESET,
            con.TEMPLATE_AUTH_PASSWORD_RESET_DONE,
            con.TEMPLATE_AUTH_PASSWORD_RESET_CONFIRM,
            con.TEMPLATE_AUTH_RESET_DONE,
        ]

        # Список HTML-шаблонов для авторизованного пользователя.
        self.template_names_authorized_users = [
            con.TEMPLATE_AUTH_PASSWORD_CHANGE,
            con.TEMPLATE_AUTH_PASSWORD_CHANGE_DONE,
        ]

        # Список адресов страниц для не авторизованного пользователя.
        self.address_page_unauthorized_users = [
            '/auth/signup/',
            '/auth/logout/',
            '/auth/login/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
            f'/auth/reset/{self.test_uidb64}/{self.test_token}/',
            '/auth/reset/done/',
        ]

        # Список адресов страниц для авторизованного пользователя.
        self.address_page_authorized_user = [
            '/auth/password_change/',
            '/auth/password_change_done/',
        ]

        # Список редиректов для авторизованного пользователя.
        self.redirects_page_authorized_user = '/auth/password_change_done/'

        # Список адресов страниц которые делают реидрект
        # для не авторизованного пользователя.
        self.addresses_page_redirects = [
            self.address_page_unauthorized_users[con.INDEX_USER_SIGNUP],
            self.address_page_unauthorized_users[con.INDEX_USER_RESET_FORM],
            self.address_page_unauthorized_users[con.INDEX_USER_RESET_CONFIRM]
        ]

        # Список редиректов для не авторизованного пользователя.
        self.redirects_page_unauthorized_user = [
            con.INDEX,
            self.address_page_unauthorized_users[con.INDEX_USER_RESET_DONE],
            (self.address_page_unauthorized_users
                [con.INDEX_USER_RESET_COMPLETE]),
        ]

    def form_post_response(self, page):
        """Функция для отправки POST-запроса с заполненой формой."""
        response = self.authorized_client.post(
            page,
            data=self.form_data,
            follow=True
        )
        return response
