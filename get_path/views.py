from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .backend import get_min_path
import json

@csrf_exempt
def get_path(request):
	if request.body:
		js = {}
		js = json.loads(request.body)

		origin = destination = None
		if 'origin' in js.keys():
			origin = js['origin']
		if 'destination' in js.keys():
			destination = js['destination']
		locations = js['cities']
		res = get_min_path(locations, origin=origin, destination=destination)
		res = {'path': res[0], 'cost': res[1]}
		
		return JsonResponse(res)
	return HttpResponse('null')

def index(request):
	return render(request, 'get_path/index.html')