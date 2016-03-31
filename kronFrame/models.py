from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Course(models.Model):
	course_name = models.CharField(max_length=100)
	course_ID = models.CharField(max_length=25)
	prereq = models.ManyToManyField("self", symmetrical=False)
	course_acronym = models.CharField(max_length=10, primary_key=True)
	CREDS = (
		(2,'2 Credits'),
		(4, '4 Credits'),
	)
	course_credits = models.IntegerField(choices=CREDS, default=4)
	def __str__(self):
		return self.course_acronym

class CallSign(models.Model):
	sign = models.CharField(max_length = 50, primary_key = True)
	def __str__(self):
		return self.sign

class Offered(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	callSign = models.ManyToManyField(CallSign)
	areaName = models.CharField(max_length=50)
	DAYS = (
		('Mon','Monday'),
		('Tue','Tuesday'),
		('Wed','Wednesday'),
		('Thu','Thursday'),
		('Fri','Friday'),
		('Sat','Saturday'),
	)
	TIME_CHOICES = (
		('1', "08:00"),
		('2', "08:30"),
		('3', "09:00"),
		('4', "09:30"),
		('5', "10:00"),
		('6', "10:30"),
		('7', "11:00"),
		('8', "11:30"),
		('9', "12:00"),
		('10', "12:30"),
		('11', "01:00"),
		('12', "01:30"),
		('13', "02:00"),
		('14', "02:30"),
		('15', "03:00"),
		('16', "03:30"),
		('17', "04:00"),
		('18', "04:30"),
		('19', "05:00"),
		('20', "05:30"),
		('21', "06:00"),
		('22', "06:30"),
	)
	class_day = models.CharField(max_length=3, choices=DAYS, default='Mon')
	start_time = models.CharField(max_length=2,choices=TIME_CHOICES, default=1)
	end_time = models.CharField(max_length=2,choices=TIME_CHOICES, default=1)
	def __str__(self):
		return str(self.course)+": "+str(self.class_day)+","+str(self.get_start_time_display())+" to "+str(self.get_end_time_display())
