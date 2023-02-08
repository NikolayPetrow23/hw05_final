from django.core.files.uploadedfile import SimpleUploadedFile

# Константы для фикстура.
USERNAME = 'author'
USERNAME_FOLLOWER = 'test-follower'
GROUP_TITLE = 'test-group'
GROUP_SLUG = 'slug'
GROUP_DESCRIPTION = 'test-description'
POST_TEXT = 'test-post'
FORM_TEXT = 'test_text_text'
FIRST_GROUP = 0
SECOND_GROUP = 1
TEXT_COMMENT = 'test-comment'

# Константа создания изображения.
small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
IMAGE = SimpleUploadedFile(
    name='small.gif',
    content=small_gif,
    content_type='image/gif'
)

# Константы количества постов.
TOTAL_POSTS = 13
PAGE_POST_TEN = 10
PAGE_POST_THREE = 3
PAGE_TWO = 2
FIRST_POST = 0
FIRST_FOLLOWING_POST = 0
LIST_PAGE_POST = [PAGE_POST_TEN, PAGE_POST_THREE]

# Константы HTML-шаблонов.
TEMPLATE_INDEX = 'posts/index.html'
TEMPLATE_POST_GROUP = 'posts/group_list.html'
TEMPLATE_POST_PROFILE = 'posts/profile.html'
TEMPLATE_POST_DETAIL = 'posts/post_detail.html'
TEMPLATE_POST_CREATE_OR_EDIT = 'posts/create_post_or_update.html'

TEMPLATE_404 = 'core/404_page_not_found.html'
TEMPLATE_403 = 'core/403_permission_denied_view.html'

# Константы адресов страниц.
INDEX = '/'
POST_CREATE = '/create/'
UNEXISTING = '/unexisting_page/'
# EXCEPTION_403 = '/exception/403/'

# Константы индексов списков spacename:name, и адресов страниц.
INDEX_NUMBER_INDEX = 0
INDEX_NUMBER_POST_GROUP = 1
INDEX_NUMBER_POST_PROFILE = 2
INDEX_NUMBER_POST_DETAIL = 3
INDEX_NUMBER_POST_CREATE = 4
INDEX_NUMBER_POST_EDIT = 5

# Константы индексов списка страниц подписок, отписок
# и страница с постами following.
INDEX_NUMB_FOLLOW = 0
INDEX_NUMB_UNFOLLOW = 1
INDEX_NUMB_POSTS_PAGE_FOLLOW = 2
