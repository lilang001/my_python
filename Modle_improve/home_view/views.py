# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from models import Person

# Create your views here.

def home(request):
    Tur = ["HTML", "CSS", "jQuery", "Python", "Django"]
    return render(request, 'home.html', {'Tur': Tur})

def tuple(request2):
    Tp = {'site': u'麦子学院', 'content': u'麦子学院之麦子圈'}
    return render(request2, 'tuple.html', {'Tp': Tp})

def list(request3):
    List = map(str, range(100))
    return render(request3, 'list.html', {'List': List})
def count(request4, a):
    c = int(a)
    return render(request4, 'grade.html', {'c': c})
def script(request4):
    List2 = ['自强学堂', '渲染Json到模板']
    return render(request4, 'script.html', {'List2': json.dumps.List2})

Person.objects.create(name="WeizhongTu", age=24)

