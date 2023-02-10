from django.core.cache import cache
from django.urls import reverse

from .fixtures import const as con
from .fixtures.fixtures_data_and_user import PostsTests
from ..models import Post, Follow


class PostsViewsTests(PostsTests):
    """Тесты для posts.views"""
    def check_page_obj_and_posts_context_views(self, post, expected_post):
        """Функция проверки соответствия полей поста."""
        self.assertEqual(
            post.pk,
            expected_post.pk
        )
        self.assertEqual(
            post.text,
            expected_post.text
        )
        self.assertEqual(
            post.author,
            expected_post.author
        )
        self.assertEqual(
            post.group,
            expected_post.group
        )
        self.assertEqual(
            post.image,
            expected_post.image
        )

    def check_group_views(self, group, index_group):
        """Функция проверки соответствия полей группы."""
        self.assertEqual(
            group.pk,
            self.group[index_group].pk
        )
        self.assertEqual(
            group.title,
            self.group[index_group].title
        )
        self.assertEqual(
            group.slug,
            self.group[index_group].slug
        )
        self.assertEqual(
            group.description,
            self.group[index_group].description
        )

    def test_posts_pages_uses_correct_template(self):
        """Проверяем, корректность вызова HTML-шаблонов."""
        templates_pages_names = dict(zip(self.pages_space_name_and_name,
                                         self.templates_names))
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_posts_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = (self.authorized_client.get(
            self.pages_space_name_and_name[con.INDEX_NUMBER_INDEX]))
        self.check_page_obj_and_posts_context_views(
            response.context['page_obj'][con.FIRST_POST],
            self.post
        )

    def test_posts_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = (self.authorized_client.get(
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_GROUP]))
        self.check_page_obj_and_posts_context_views(
            response.context['page_obj'][con.FIRST_POST],
            self.post
        )
        self.check_group_views(response.context['group'], con.FIRST_GROUP)

    def test_posts_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = (self.authorized_client.get(
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_PROFILE])
        )
        self.check_page_obj_and_posts_context_views(
            response.context['page_obj'][con.FIRST_POST],
            self.post
        )
        self.assertEqual(response.context['author'], self.user)

    def test_posts_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.get(
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_DETAIL]
        ))
        self.check_page_obj_and_posts_context_views(
            response.context['post'],
            self.post
        )

    def test_posts_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_CREATE]
        )
        self.assertIsInstance(response.context['form'], self.form_views)

    def test_posts_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = (self.authorized_client.get(
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_EDIT]
        ))
        self.check_page_obj_and_posts_context_views(
            response.context['post'],
            self.post
        )
        self.assertIsInstance(response.context['form'], self.form_views)

    def test_posts_correct_paginator_page(self):
        """Проверка пагинатора."""
        gen_posts = [Post(author=self.user,
                          text=f'test-text {x}',
                          group=self.group[con.FIRST_GROUP]
                          ) for x in range(12)]
        Post.objects.bulk_create(gen_posts)
        for page in self.page_check_paginator_and_add_post:
            for page_numb in range(con.PAGE_TWO):
                with self.subTest(page=page):
                    response = self.authorized_client.get(
                        page, {'page': page_numb + 1}
                    )
                    self.assertEqual(
                        len(response.context['page_obj']),
                        con.LIST_PAGE_POST[page_numb]
                    )

    def test_posts_create_correct_new_post(self):
        """
        Проверка того, что пост не попал в группу,
        которой он не принадлежит.
        """
        response_group = self.authorized_client.get(reverse(
            'posts:group_list', args=(self.group[con.SECOND_GROUP].slug,)
        ))
        self.assertNotEqual(
            response_group.context['page_obj'],
            self.post
        )

    def test_posts_cache_index_page(self):
        """Проверяем, кэширование на странице index."""
        response_old_page = self.authorized_client.get(
            self.pages_space_name_and_name[con.INDEX_NUMBER_INDEX]
        )
        post_old = response_old_page.content

        Post.objects.last().delete()

        # Проверка на то, что пост остался в кэшэ, после удаления поста.
        response_expected_cache = self.authorized_client.get(
            self.pages_space_name_and_name[con.INDEX_NUMBER_INDEX]
        )
        post_expected_cache = response_expected_cache.content
        self.assertEqual(post_old, post_expected_cache)

        cache.clear()

        # Проверка на то, что пост не осталася на странице,
        # после очищения кэша.
        response_del_post = self.authorized_client.get(
            self.pages_space_name_and_name[con.INDEX_NUMBER_INDEX]
        )
        post_del_post = response_del_post.content
        self.assertNotEqual(post_expected_cache, post_del_post)

    def test_subscription_author(self):
        """
        Проверяем, что авторизованный пользователь может подписываться
        на других пользователей.
        """
        follow_related_count = Follow.objects.count()

        self.authorized_client.get(
            self.page_subscriptions[con.INDEX_NUMB_FOLLOW]
        )
        self.assertEqual(Follow.objects.count(), follow_related_count + 1)

    def test_author_unsubscribes(self):
        """
        Проверяем, что авторизованный пользователь может отписываться
        от других пользователей.
        """
        follow_related_count = Follow.objects.count()

        Follow.objects.create(
            user=self.user,
            author=self.user_follower
        )

        self.authorized_client.get(
            self.page_subscriptions[con.INDEX_NUMB_UNFOLLOW]
        )

        self.assertEqual(Follow.objects.count(), follow_related_count)

    def test_you_can_subscribe_to_yourself(self):
        """Проверяем что нельзя подписаться на самого себя."""
        follow_related_count = Follow.objects.count()

        self.authorized_client.get(reverse(
            'posts:profile_follow',
            args=(self.user.username,)))

        self.assertEqual(Follow.objects.count(), follow_related_count)

    def test_you_can_subscribe_only_once(self):
        """Проверяем что можно подписаться только один раз."""
        follow_related_count = Follow.objects.count()
        for follow in range(4):
            self.authorized_client.get(
                self.page_subscriptions[con.INDEX_NUMB_FOLLOW]
            )
        self.assertEqual(Follow.objects.count(), follow_related_count + 1)

    def test_shows_post_follow_index(self):
        """
        Проверяем, что новая запись пользователя появляется в ленте тех,
        кто на него подписан.
        """
        post = self.creation_post(self.user_follower)

        Follow.objects.create(
            user=self.user,
            author=self.user_follower
        )

        follow_index = self.authorized_client.get(
            self.page_subscriptions[con.INDEX_NUMB_POSTS_PAGE_FOLLOW]
        )

        self.check_page_obj_and_posts_context_views(
            follow_index.context['page_obj'][con.FIRST_FOLLOWING_POST],
            post
        )

    def test_does_not_show_post_follow_index(self):
        """
        Проверяем, что запись не появляется в ленте тех, кто не подписан.
        """
        post = self.creation_post(self.user_follower)
        unfollow_index = self.authorized_client.get(
            self.page_subscriptions[con.INDEX_NUMB_POSTS_PAGE_FOLLOW]
        )
        self.assertNotEqual(
            unfollow_index.context['page_obj'], post
        )
