from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .plot import plot
import json

@csrf_exempt
def get_path(request):
	if request.body:
		points = json.loads(request.body)['points']
		res = plot(points)
		with open('tmp', 'w') as f:
			f.write(res)
		return HttpResponse(res)
	return HttpResponse('null')