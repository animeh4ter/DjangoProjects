from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_profiles(request, profiles, results):
    page = request.GET.get('page', 1)
    # result = 6
    paginator = Paginator(profiles, results, allow_empty_first_page=False)
    # code for older django with page method in projects/utils
    profiles = paginator.get_page(page)

    left_index = int(page) - 4

    if left_index < 1:
        left_index = 1

    right_index = int(page) + 5

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, profiles


def search_profile(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skill = Skill.objects.filter(name__icontains=search_query)
    profile = Profile.objects.distinct().filter(Q(name__icontains=search_query) |
                                                Q(short_intro__icontains=search_query) |
                                                Q(skill__in=skill))
    return profile, search_query
