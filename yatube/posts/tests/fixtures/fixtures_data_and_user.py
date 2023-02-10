import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from . import const as con
from ...forms import PostForm
from ...models import Post, Group

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=con.USERNAME)
        cls.user_follower = User.objects.create_user(
            username=con.USERNAME_FOLLOWER
        )

        cls.group = [Group.objects.create(
            title=f'{con.GROUP_TITLE}{x}',
            slug=f'{con.GROUP_SLUG}{x}',
            description=f'{con.GROUP_DESCRIPTION}{x}') for x in range(2)]

        cls.post = Post.objects.create(
            author=cls.user,
            text=con.POST_TEXT,
            group=cls.group[con.FIRST_GROUP],
            image=con.IMAGE
        )

        # Объкты форм.
        cls.form_views = PostForm
        cls.form_forms = PostForm()
        cls.form_data = {
            'text': con.FORM_TEXT,
            'group': cls.group[con.FIRST_GROUP].pk,
            'image': con.IMAGE
        }
        cls.form_comment = {
            'post': cls.post.id,
            'author': cls.user.id,
            'text': con.TEXT_COMMENT,
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        # Список адресов страниц.
        self.address_page_url = [
            con.INDEX,
            f'/group/{self.group[con.FIRST_GROUP].slug}/',
            f'/profile/{self.post.author.username}/',
            f'/posts/{self.post.pk}/',
            con.POST_CREATE,
            f'/posts/{self.post.pk}/edit/',
        ]

        # Список достпных страниц для не авторизованного пользователя.
        self.address_page_unauthorized_user = [
            self.address_page_url[con.INDEX_NUMBER_INDEX],
            self.address_page_url[con.INDEX_NUMBER_POST_GROUP],
            self.address_page_url[con.INDEX_NUMBER_POST_PROFILE],
            self.address_page_url[con.INDEX_NUMBER_POST_DETAIL],
        ]

        # Список HTML-шаблонов страниц posts.
        self.templates_names = [
            con.TEMPLATE_INDEX,
            con.TEMPLATE_POST_GROUP,
            con.TEMPLATE_POST_PROFILE,
            con.TEMPLATE_POST_DETAIL,
            con.TEMPLATE_POST_CREATE_OR_EDIT,
            con.TEMPLATE_POST_CREATE_OR_EDIT,
        ]

        # Список spacename:name адресов страниц.
        self.pages_space_name_and_name = [
            reverse('posts:index'),
            reverse('posts:group_list',
                    args=(self.group[con.FIRST_GROUP].slug,)),
            reverse('posts:profile', args=(self.post.author,)),
            reverse('posts:post_detail', args=(self.post.pk,)),
            reverse('posts:post_create'),
            reverse('posts:post_edit', args=(self.post.pk,)),
            reverse('posts:add_comment', args=(self.post.pk,))
        ]

        # Список для проверки пагинатора и добовления поста на разные страницы.
        self.page_check_paginator_and_add_post = [
            self.pages_space_name_and_name[con.INDEX_NUMBER_INDEX],
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_GROUP],
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_PROFILE],
        ]

        # Список spacename:name подписки,
        # отписки и страница с постами following.
        self.page_subscriptions = [
            reverse('posts:profile_follow',
                    args=(self.user_follower.username,)),
            reverse('posts:profile_unfollow',
                    args=(self.user_follower.username,)),
            reverse('posts:follow_index'),
        ]

    def form_post_response(self, page, form):
        """Функция для отправки POST-запроса с заполненой формой."""
        response = self.authorized_client.post(
            page,
            data=form,
            follow=True
        )
        return response

    def creation_post(self, user):
        """Функция создания поста."""
        post = Post.objects.create(
            author=user,
            text=con.POST_TEXT,
            group=self.group[con.SECOND_GROUP],
            image=con.IMAGE)
        return post
