from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .plot import plot
import json

@csrf_exempt
def get_path(request):
	coordinates = []

	if request.method == 'GET':
		return

	if request.method == 'POST':
		coordinates = json.loads(request.POST.get('coordinates'))

	res = plot(coordinates)

	return HttpResponse(res)