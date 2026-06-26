from django.core.paginator import Paginator

PAGE_SIZE = 12


def paginate(request, queryset, per_page=PAGE_SIZE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page', 1))
