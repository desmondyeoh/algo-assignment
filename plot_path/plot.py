# -*- coding: utf-8 -*-
from gmplot import gmplot

from . import gpolyline_decoder as gd
import googlemaps


gmaps = googlemaps.Client(key='AIzaSyDH-tcLsms99nDpPJOsd_tVGRUtZsgDkrU')


def plot(list_c):
	color = ['red', 'orange', 'blue', 'magenta', 'lime', 'brown', 'purple']
	l1, l2 = latlng_list(list_c[0], list_c[1])
	gm = gmplot.GoogleMapPlotter(list_c[0][0], list_c[0][1], 15)
	gm.marker(l1[0], l2[0], color[0])
	gm.plot(l1, l2, color[1], edge_width = 8)
	gm.marker(l1[len(l1) - 1], l2[len(l2) - 1], color[1])
	n = 2
	for x in range(1, len(list_c) - 1):	
		l1, l2 = latlng_list(list_c[x], list_c[x + 1])
		gm.plot(l1, l2, color[n], edge_width = 8)
		gm.marker(l1[len(l1) - 1], l2[len(l2) - 1], color[n])
		n += 1
		if n == len(color):
			n = 0
	gm.draw = draw
	output = VirtualFile()
	gm.draw(gm, output)
	return output.flush()


def latlng_list(origin, destination):
	latlngs = gd.decode_line(get_json_dir_str(origin, destination))
	l1, l2 = zip(*latlngs)
	return l1, l2


def get_json_dir_str(origin, destination):
	directions_result = gmaps.directions(origin, destination, mode = "driving")
	direction_json = directions_result[0]["overview_polyline"]["points"]
	return direction_json


class VirtualFile:

	def __init__(self):
		self.txt = ''

	def write(self, args):
		if type(args) != str:
			raise Exception("'write()' require string but other type found")
		self.txt += args
		return len(args)

	def flush(self):
		return self.txt


def draw(self, virtual_file):
	f = virtual_file
	html_str = '<html>\n<head>\n<meta name="viewport" content="initial-sc' + \
			   'ale=1.0, user-scalable=no" />\n<meta http-equiv="content-' + \
			   'type" content="text/html; charset=UTF-8"/>\n<title>Google' + \
			   ' Maps - pygmaps </title>\n'
	f.write(html_str)
	if self.apikey:
	    f.write('<script type="text/javascript" src="https://maps.googlea' + \
	    		'pis.com/maps/api/js?libraries=visualization&sensor=true_' + \
	    		'or_false&key=%s"></script>\n' % self.apikey )
	else:
	    f.write('<script type="text/javascript" src="https://maps.googlea' + \
	    		'pis.com/maps/api/js?libraries=visualization&sensor=true_' + \
	    		'or_false"></script>\n' )

	f.write('<script type="text/javascript">\n\tfunction initialize() {\n')
	self.write_map(f)
	self.write_grids(f)
	self.write_points(f)
	self.write_paths(f)
	self.write_shapes(f)
	self.write_heatmap(f)
	html_str = '\t}\n</script>\n</head>\n<body style="margin:0px; padding' + \
			   ':0px;" onload="initialize()">\n\t<div id="map_canvas" sty' + \
			   'le="width: 100%; height: 100%;"></div>\n</body>\n</html>\n'
	f.write(html_str)