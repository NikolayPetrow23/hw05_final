from django.shortcuts import render


def page_not_found(request, exception):
    return render(request,
                  'core/404_page_not_found.html',
                  {'path': request.path},
                  status=404)


def server_error(request):
    return render(request, 'core.500.html', status=500)


def csrf_failure(request, reason=''):
    return render(request, 'core/403_csrf.html')


def permission_denied(request, exception):
    return render(request,
                  'core/403_permission_denied_view.html',
                  status=403)
