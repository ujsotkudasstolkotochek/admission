from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from parsers.models import Program

def home(request):
    return render(request, 'core/home.html')

def programs_stats_api(request):
    programs = Program.objects.all().order_by('code')
    html = render_to_string('core/table_partial.html', {'programs': programs})
    return HttpResponse(html)