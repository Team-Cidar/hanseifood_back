from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt,name='dispatch')
def index(request):
    return HttpResponse("Hello world!")