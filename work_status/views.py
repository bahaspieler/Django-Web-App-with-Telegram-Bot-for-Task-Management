from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from .models  import *
from .forms import *
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import re


p_site= re.compile(r's', re.I)
p_date= re.compile(r'dt', re.I)
p_exc= re.compile(r'exe', re.I)
p_service= re.compile(r'service', re.I)
p_type= re.compile(r'type', re.I)
p_task= re.compile(r'task', re.I)
p_dom= re.compile(r'dom', re.I)
p_remarks= re.compile(r'rem', re.I)


# Create your views here.



def home(request):
    items = team.objects.all()
    context = {
        'items' : items,
    }
    return render(request, 'home.html', context)

@login_required
def display_lte(request):
    items = lte_integration.objects.all().order_by('-id')
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
        # filter = 'CXMRD1'
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

def add_lte(request):
    if request.method == 'POST':
        form = LteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('validate')

    else:
        form = LteForm()

        return render(request, 'add_new.html', {'form': form})


def instance(request, pk):
    item= get_object_or_404(lte_validation, pk=pk)
    return item

def edit_lte(request, pk):
    item= get_object_or_404(lte_integration, pk=pk)
    # item= lte_integration.objects.filter(id=pk).defer('id').first()

    if request.method == "POST":
        form= LteForm(request.POST,instance=item) #auto_id=False  for label

        if form.is_valid():


            # f.remove('id')

            form.save()

            return redirect('display_lte')

    else:
        form= LteForm(instance=item)

        return render(request, 'edit_item.html', {'form': form})


# def edit_lte(request, pk):
#     # item= get_object_or_404(lte_integration, pk=pk)
#     item= lte_validation.objects.filter(id=pk).defer('id').first()
#
#     if request.method == "POST":
#         form= LteForm(request.POST,instance=item) #auto_id=False  for label
#
#         if form.is_valid():
#             f=form.save(commit=False)
#
#             # f.remove('id')
#
#             f.save()
#             print(f.id)
#
#             return redirect('display_lte')
#
#     else:
#         form= LteForm(instance=item)
#
#         return render(request, 'edit_item.html', {'form': form})


def delete_lte(request, pk):
    lte_integration.objects.filter(id=pk).delete()

    items= lte_integration.objects.all()

    context = {

        'items' : items
    }

    return render(request, 'index.html', context)





