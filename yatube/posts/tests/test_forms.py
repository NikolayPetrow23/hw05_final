from .fixtures import const as con
from .fixtures.fixtures_data_and_user import PostsTests
from ..models import Post, Comment


class PostsFormsTests(PostsTests):
    """Тесты для posts.forms"""
    def test_posts_forms_correct_add(self):
        """Проверяем, корректность добавлнеия поста через форму."""
        posts_count = Post.objects.count()
        # Вызов функции для отправки POST-запроса.
        response = self.form_post_response(
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_CREATE],
            self.form_data
        )

        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(
            response,
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_PROFILE]
        )

    def test_posts_forms_correct_edit(self):
        """Проверяем, корректность редактирования поста через форму."""
        posts_count = Post.objects.count()
        # Форма для проверки измененя группы
        form_data_two = {
            'text': con.FORM_TEXT,
            'group': self.group[con.SECOND_GROUP].pk
        }
        # Вызов функции для отправки POST-запроса.
        response = self.form_post_response(
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_EDIT],
            form_data_two
        )

        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(Post.objects.all()[con.FIRST_POST].text,
                         con.FORM_TEXT)
        self.assertEqual(Post.objects.all()[con.FIRST_POST].group,
                         self.group[con.SECOND_GROUP])
        self.assertRedirects(
            response,
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_DETAIL]
        )

    def test_not_adding_comments_unauthorized_user(self):
        """
        Проверка, на то что коментировать может
        только авторизованный пользователь
        """
        # Отправляем POST-запрос с заполненой формой,
        # не авторизованным пользователем.
        response = self.guest_client.post(
            self.pages_space_name_and_name[con.INDEX_NUMBER_POST_DETAIL],
            data=self.form_comment,
            follow=True
        )
        self.assertNotContains(response, con.TEXT_COMMENT)

    def test_correct_add_comment_post(self):
        """
        Проверка, на корректное добавление
        комментария на страницу post_detail и в БД.
        """
        comments_count = Comment.objects.count()

        # Отправляем POST-запрос с заполненной формой.
        response = self.form_post_response(
            self.pages_space_name_and_name[con.INDEX_NUMBER_ADD_COMMENT],
            self.form_comment
        )

        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertContains(response, con.TEXT_COMMENT)
