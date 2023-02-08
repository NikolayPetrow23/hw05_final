from django.core.paginator import Paginator

LAST_TEN_POSTS = 10


def paginator_view(request, posts_list):
    paginator = Paginator(posts_list, LAST_TEN_POSTS)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    return page_objects
