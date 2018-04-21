from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .backend import get_min_path
import json

def hello(requests):
	return HttpResponse("hi")
@csrf_exempt
def get_path(request):
	param = {}

	if request.method == 'GET':
		return

	if request.method == 'POST':
		param = request.POST

	origin = destination = None
	if 'origin' in param:
		origin = param.get('origin')
	if 'destination' in param:
		destination = param('destination')
	locations = json.loads(param.get('cities'))

	res = get_min_path(locations, origin=origin, destination=destination)
	res = {'path': res[0], 'cost': res[1]}

	return JsonResponse(res)