from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
# Create your models here.

class lte_integration(models.Model):
    site= models.CharField(max_length=10, blank= True)
    service= models.CharField(max_length=5, blank=True)
    type=models.CharField(max_length=100, blank= True)
    task=models.CharField(max_length=100, blank= True)
    date=models.DateField(default= datetime.now(),blank= True)
    executor=models.CharField(max_length=100, blank= True)
    domain = models.CharField(max_length=100, blank=True)
    ticket = models.CharField(max_length=100, blank=True)
    remarks=models.CharField(max_length=200)
    time= models.TimeField(default=datetime.now(), blank= True)


    def __str__(self):
        return 'Site/Cell Name : {0} Service type : {1} Task Type : {2} Task Details : {3} Execution Date : {4} Executor Name : {5} InC Domain : {6} Ticket No. : {7} Remarks : {8} '.format(self.site, self.service, self.type, self.task, self.date, self.executor, self.domain, self.ticket, self.remarks)


class lte_validation(models.Model):
    executor = models.CharField(max_length=100, blank= True)
    ticket = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=100, blank=True)
    date = models.DateField(default=datetime.now(), blank=True)
    domain = models.CharField(max_length=30, blank=True)
    choices= (('1','Bulk'), ('2','Major'), ('3','Critical'))
    catag= models.CharField(max_length=20, choices=choices, blank=True)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return  'Executor : {0} Ticket No. : {1} Task Type : {2} Execution Date : {3} InC Domain : {4}'.format(self.executor, self.ticket, self.type, self.date, self.domain)


class team(models.Model):
    name= models.CharField(max_length=30, blank=False)
    designation= models.CharField(max_length=30, blank=False)
    email= models.EmailField(max_length=300, blank=False)
    contact = models.CharField(max_length=15)
    image = models.ImageField(default='default.jpg', upload_to='Team')
    def __str__(self):
        return 'Name: {0} Designation: {1}'.format(self.name, self.designation)

class prs(models.Model):
    pre_data = models.FileField(upload_to='PRS')
    post_data = models.FileField(upload_to='PRS')
    site_list= models.FileField(upload_to='PRS')
    threshold = models.FileField(upload_to='PRS')
    choices= (('1','2G'), ('2','3G'), ('3','4G'))
    type= models.CharField(max_length=5,choices=choices, blank=False)



