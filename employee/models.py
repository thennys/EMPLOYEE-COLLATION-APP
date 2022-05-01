
from django.db import models

import random
# Create your models here.

FRONTEND = 'FR'
BACKEND = 'SO'
JUNIOR = 'JR'
SENIOR = 'SR'
BOSS = 'B'

POSITION_CHOICES = [
        (FRONTEND, 'frontend'),
        (BACKEND, 'backend'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (BOSS , 'boss'),
    ]
""" DATABASE FOR  EMPLOYEES"""
""" Employee code is the required argument for creating supervisor """
class Supervisors(models.Model):
	supervisor  		= models.CharField(max_length=100)

	def __str__(self):
		return self.supervisor
	
	class Meta:
		verbose_name_plural = "Supervisors"

class EmployeeRecords(models.Model):
	first_name 			= models.CharField(max_length=255)
	middle_name			= models.CharField(max_length=255)
	date_of_graduation  = models.DateField()
	date_of_employment  = models.DateField()
	position            = models.CharField(max_length=255,choices=POSITION_CHOICES,default=FRONTEND)
	salary 				= models.IntegerField()
	supervisors 		= models.ManyToManyField(Supervisors,blank=True)
	employee_code 		= models.CharField(max_length=6,blank=True, null=True)
	
	def save(self, *args, **kwargs):
		getThreeRandomNumbers   	  	= "".join(random.choice("0123456789") for i in range(3))
		generatedEmployeeCode  			= self.first_name[:1]+self.middle_name[:1]+'-'+getThreeRandomNumbers
		self.employee_code 				= generatedEmployeeCode
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.first_name+self.middle_name}"

	class Meta:
		verbose_name_plural = "Employee Records"



"""Logss upload models """
class UploadLogs(models.Model):
	timestamp_of_upload 				= models.DateTimeField(auto_now_add=True)
	number_of_employee_records_uploaded = models.IntegerField()
	status 								= models.CharField(max_length=100)
	errors 								= models.CharField(max_length=100, blank=True, null=True)
	number_of_duplicate_entries 		= models.IntegerField()

	def __str__(self):
		return f"{self.status}"

	class Meta:
		verbose_name_plural = "Upload logs"
