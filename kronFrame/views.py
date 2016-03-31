from django.shortcuts import render
from django.views import generic
from collections import OrderedDict
from django.http import HttpResponse, HttpResponseRedirect

from .models import Offered, Course
from pprint import pprint
import pygraphviz as pgv

from .models import Course

class IndexView(generic.ListView):
	template_name = 'kronFrame/index.html'
	context_object_name = 'courseList'

	def get_queryset(self):
		courseList = {}
		for x in Offered.objects.all():
			if x.course not in courseList: courseList[x.course] = [x]
			else: courseList[x.course].append(x)
		print courseList
		return courseList

class HomeView(generic.ListView):
	template_name = 'kronFrame/home.html'
	context_object_name = 'dataSet'

	def get_queryset(self):
		dataSet = {}
		dataSet['table'] = OrderedDict([('Mon',OrderedDict()),('Tue',OrderedDict()),('Wed',OrderedDict()),('Thu',OrderedDict()),('Fri',OrderedDict()),('Sat',OrderedDict())])
		dataSet['ourDays'] = dict([('Mon',"Monday"),('Tue',"Tuesday"),('Wed',"Wednesday"),('Thu',"Thursday"),('Fri',"Friday"),('Sat',"Saturday")])
		dataSet['choice'] = set()
		dataSet['times'] = [" "]
		for x in range(1,len(Offered.TIME_CHOICES)):
			dataSet['times'].append(Offered.TIME_CHOICES[x][1])
		for day in dataSet['table'].keys():
			for seg in range(20):
				dataSet['table'][day][seg+2] = []
		for x in Offered.objects.all():
			for allSeg in range(int(x.start_time),int(x.end_time)):
				if(x.course.course_acronym not in dataSet['table'][x.class_day][allSeg]):
					x.woah = ""
					for y in x.callSign.all():
						dataSet['choice'].add(y.sign)
						x.woah += y.sign+" "
					dataSet['table'][x.class_day][allSeg].append(x)
		dataSet['choice'] = sorted(list(dataSet['choice']))
		pprint(dataSet['choice'])
		return dataSet

def subgraph(request):
	subjectList = []
	for i in range(1,11):
		subjectList.append(request.POST.getlist('Subject%d' % (i)))
	subjectList = [item for sublist in subjectList for item in sublist if item != '-----']
	print 'subjectlist', subjectList
	courseList = [min(map(lambda x: x.course, Offered.objects.filter(callSign=subject)), key=lambda x: x.course_acronym)
					for subject in subjectList]
	print 'courseList', courseList
	svg_data = courses_to_SVG(courseList)
	return HttpResponse(svg_data, content_type='image/svg+xml')

# Dependency graph helper functions
def add_edges(course, edges):
	prereqs = course.prereq.all()
	if prereqs == []:
		return
	else:
		for pr in prereqs:
			edges.append((pr, course))
			add_edges(pr, edges)
		return

def courses_to_SVG(courses):
	edges = []
	for course in courses:
		add_edges(course, edges)
	nodes = set([n1 for n1, n2 in edges] + [n2 for n1, n2 in edges] + courses)

	G = pgv.AGraph(directed=True)
	for node in nodes:
		G.add_node(node, label=node.course_ID + '\n' + node.course_acronym, id=node.course_ID)

	for edge in edges:
		G.add_edge(edge[0], edge[1])

	svg_data = G.draw(prog='dot', format='svg')
	return svg_data
