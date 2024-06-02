from django.shortcuts import render

from http import HTTPStatus


def page_not_found(request, exception):
    template = 'pages/404.html'
    return render(request, template, status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=''):
    template = 'pages/403csrf.html'
    return render(request, template, status=HTTPStatus.FORBIDDEN)


def forbidden(request, exception):
    template = 'pages/403.html'
    return render(request, template, status=HTTPStatus.FORBIDDEN)


def server_error(request):
    template = 'pages/500.html'
    return render(request, template, status=HTTPStatus.INTERNAL_SERVER_ERROR)
