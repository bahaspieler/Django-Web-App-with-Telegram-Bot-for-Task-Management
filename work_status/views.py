from django.core.files import File
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from .models  import *
from .forms import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import re
import pandas as pd
import numpy as np
from tabulate import tabulate as tb
from .prsbot import prsdata
import os
from django.conf import settings
import mimetypes
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str



p_site= re.compile(r's', re.I)
p_date= re.compile(r'dt', re.I)
p_exc= re.compile(r'exe', re.I)
p_service= re.compile(r'service', re.I)
p_type= re.compile(r'type', re.I)
p_task= re.compile(r'task', re.I)
p_dom= re.compile(r'dom', re.I)
p_remarks= re.compile(r'rem', re.I)


def group_check(user):
    return user.groups.filter(name='InC').exists()


@user_passes_test(group_check, login_url='display_lte')
def edit_lte(request, pk):
    item= get_object_or_404(lte_integration, pk=pk)
    # item= lte_integration.objects.filter(id=pk).defer('id').first()

    if request.method == "POST":
        form= LteForm(request.POST,instance=item) #auto_id=False  for label

        if form.is_valid():
            form.save()
            return redirect('display_lte')

    else:
        form= LteForm(instance=item)

        return render(request, 'edit_item.html', {'form': form})


def prs_analysis(request):

    items = get_object_or_404(prs, pk=1)
    if request.method == 'POST':

        form = PRSuploadForm(request.POST, request.FILES, instance=items)

        if form.is_valid():
            form.save()

        # items= prs.objects.get(pk=1)
        base= settings.MEDIA_ROOT
        ultimate_f= 'PRS\\ultimate.xlsx'

        ult_p = os.path.join(base, ultimate_f)
        pre_data_p=items.pre_data.path
        post_data_p= items.post_data.path
        site_list_p= items.site_list.path
        th_p= items.threshold.path
        # ult_p = 'C:\\Users\\bahauddin\\Desktop\\Telegrambot+django\\database\\media\\PRS\\3g ultimate.xlsx'

        if items.type == '2':
            print('loop begin')
            prsdata.three(pre_data_p, post_data_p,th_p,ult_p, site_list_p)

    else:
        form = PRSuploadForm(instance=items)

    context= {
        'form': form
    }
    return render(request, 'prs.html', context)


def download(request,path, file_name):
    dir= os.path.join(settings.MEDIA_ROOT, path)
    file_path = dir +'/' + file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response



def tool(request):
    return render(request, 'tool.html')





# Create your views here.




def home(request):
    items = team.objects.all()
    context = {
        'items' : items,
    }
    return render(request, 'home.html', context)

def the_team(request):
    items = team.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'team.html', context)



@login_required
def display_lte(request):
    items_list = lte_integration.objects.all().order_by('-id')
    paginator = Paginator(items_list, 8) # Show 25 contacts per page

    page = request.GET.get('page')
    items = paginator.get_page(page)
    form = ComputerSearchForm(request.POST or None)
    context = {
        'items' : items,
        'header': 'LTE Integration',
        'form': form,

    }
    if request.method == 'POST':
        items = lte_integration.objects.all().order_by('-date').filter(
            site__icontains=form['site'].value(), service__icontains=form['service'].value(),
            type__icontains=form['type'].value(), task__icontains=form['task'].value(),
            date__icontains=form['date'].value(), executor__icontains=form['executor'].value())
        context = {
            "items": items,
            "form": form,
        }


    return render(request, 'index.html', context)

@login_required
def validate(request):
    filter = lte_validation.objects.all().order_by('-date')
    form= ValidSearchForm(request.POST or None)
    invalid= []
    for items in filter:
        if lte_integration.objects.filter(executor__icontains=items.executor, ticket__icontains=items.ticket, type__icontains=items.type, date=items.date):
            items.completed = True
            comp = items
            invalid.append(comp)
        else:
            items.completed = False
            inv = items
            invalid.append(inv)

    context ={
        "invalid": invalid,
        "form": form,
    }

    if request.method == 'POST':
        print(form)
        invalid= []
        filter= lte_validation.objects.all().order_by('-date').filter(
            executor__icontains=form['executor'].value(), date__icontains=form['date'].value(), domain__icontains=form['domain'].value()
        )

        for items in filter:
            if lte_integration.objects.filter(executor__icontains=items.executor, ticket__icontains=items.ticket,
                                              type__icontains=items.type, date=items.date):
                items.completed = True
                comp = items
                invalid.append(comp)
            else:
                items.completed = False
                inv = items
                invalid.append(inv)
        context={
            "invalid":invalid,
            "form": form,
        }
    return render(request, 'valid.html', context)


class GetList(APIView):
    def get(self,request):
        data = {'list' : []}
        button= lte_integration.objects.all()
        field= [f.name for f in lte_integration._meta.get_fields()]
        for i in field:
            data['list'].append({'name':i})
        return Response(data)

class GetFieldList(APIView):
    def post(self,request):
        data = json.loads(request.body)
        filter = data['text'].split()
        print(filter)
        try:
            if p_site.match(filter[0]):
                text1 = lte_integration.objects.all().order_by('-date').filter(site__icontains=filter[1])
                text= list(text1.values('site', 'service', 'type','task', 'date', 'executor', 'remarks', 'time'))

            elif p_date.search(filter[0]):
                text1 = lte_integration.objects.all().order_by('-date').filter(date__icontains=filter[1])
                text = list(text1.values('site', 'service', 'type','task', 'date', 'executor', 'remarks', 'time'))

            elif p_exc.match(filter[0]):
                text1 = lte_integration.objects.all().order_by('-date').filter(executor__icontains=filter[1])
                text = list(text1.values('site', 'service', 'type','task', 'date', 'executor', 'remarks', 'time'))

            elif p_service.match(filter[0]):
                text1 = lte_integration.objects.all().order_by('-date').filter(service__icontains=filter[1])
                text = list(text1.values('site', 'service', 'type','task', 'date', 'executor', 'remarks', 'time'))

            elif p_dom.match(filter[0]):
                text1 = lte_integration.objects.all().order_by('-date').filter(domain__icontains=filter[1])
                text = list(text1.values('site', 'service', 'type','task', 'date', 'executor', 'remarks', 'time'))

            elif p_task.match(filter[0]):
                text1 = lte_integration.objects.all().order_by('-date').filter(task__icontains=filter[1])
                text = list(text1.values('site', 'service', 'type','task', 'date', 'executor', 'remarks', 'time'))

            elif p_type.match(filter[0]):
                text1 = lte_integration.objects.all().order_by('-date').filter(type__icontains=filter[1])
                text = list(text1.values('site', 'service', 'type','task', 'date', 'executor', 'remarks', 'time'))

            elif p_remarks.match(filter[0]):
                text1 = lte_integration.objects.all().order_by('-date').filter(remarks__icontains=filter[1])
                text = list(text1.values('site', 'service', 'type','task', 'date', 'executor', 'remarks', 'time'))

            else:
                text = "Please enter the correct value"

            return Response({"text":text,"code":200})

        except:
            return Response({"code":401})






def todo_pending(request, pk):
    todo = lte_validation.objects.get(id=pk)
    todo.completed = False
    todo.save()
    return redirect('validate')


def todo_completed(request, pk):
    todo = lte_validation.objects.get(id=pk)
    todo.completed = True
    todo.save()
    return redirect('validate')


# @permission_required('work_status.can_add', raise_exception=True)
@user_passes_test(group_check, login_url='validate')
def add_lte(request):

    if request.method == 'POST':
        form = LteForm(request.POST)

        if form.is_valid():
            add=form.save()
            print(add.pk)
            return redirect('validate')

    else:
        form = LteForm()

        return render(request, 'add_new.html', {'form': form})


def instance(request, pk):
    item= get_object_or_404(lte_validation, pk=pk)
    return item





@user_passes_test(group_check, login_url='display_lte')
def delete_lte(request, pk):
    lte_integration.objects.filter(id=pk).delete()

    items= lte_integration.objects.all()

    context = {

        'items' : items
    }

    return render(request, 'index.html', context)





