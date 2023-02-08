# from django.contrib.auth import get_user_model
# from django.urls import reverse
#
# from .fixtures.fixtures_user import UsersTests
#
# User = get_user_model()
#
#
# class UsersFormsTests(UsersTests):
#     """."""
#     def test_user_forms_correct_add_user(self):
#         """."""
#         users_count = User.objects.count()
#         self.form_post_response(reverse('users:signup'))
#         self.assertEqual(User.objects.count(), users_count + 1)
