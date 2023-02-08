from .fixtures.fixtures_data_and_user import PostsTests
from .fixtures import const as con


class PostsModelsTests(PostsTests):
    """Тесты для posts.models"""
    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = self.group[con.FIRST_GROUP]
        post = self.post

        objects_names = {
            group: str(group),
            post: str(post)[:15],
        }

        for objects, name in objects_names.items():
            with self.subTest(objects=objects):
                self.assertEqual(objects.__str__(), name)

    def test_models_have_correct_help_text(self):
        """Проверяем, что у моделей корректно работает help_text."""
        post = self.post
        field_help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)

    def test_models_have_correct_verbose_name(self):
        """Проверяем, что у моделей корректно работает verbose_name."""
        post = self.post
        field_verboses = {
            'text': 'Введите текст',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Выберите группу',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)
