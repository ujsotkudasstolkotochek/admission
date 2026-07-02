# core/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from parsers.models import Program

def home(request):
    return render(request, 'core/home.html')

def programs_stats_api(request):
    programs = Program.objects.select_related('university').all().order_by('university__name', 'code')

    user_score = None
    user_status = 'common'  # статус пользователя по умолчанию
    show_place = False

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        profile = request.user.profile
        if profile.score is not None:
            user_score = profile.score
            user_status = profile.status or 'common'  # если не задан, считаем common
            show_place = True

    universities_data = {}
    for program in programs:
        uni_name = program.university.name
        if uni_name not in universities_data:
            universities_data[uni_name] = []

        if show_place and user_score is not None:
            # Фильтруем абитуриентов с таким же статусом и баллом > 0
            applicants = program.applicants.filter(status=user_status, score__gt=0)
            above = applicants.filter(score__gt=user_score).count()
            place = above + 1
            program.user_place = place
            program.user_total = applicants.count()
        else:
            program.user_place = None
            program.user_total = 0

        universities_data[uni_name].append(program)

    html = render_to_string('core/table_partial.html', {
        'universities_data': universities_data,
        'show_place': show_place,
    })
    return HttpResponse(html)