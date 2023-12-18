from django.db import models
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.shortcuts import render


class Food(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(max_length=100)
    food_choices = [
        ('FR', 'fruits'),
        ('VE', 'Vegetable'),
        ('ME', 'Meat'),
        ('DA', 'Dairy'),
        ('GR', 'grain'),
    ]
    status = models.CharField(max_length=10, choices=food_choices)

    def index1(request):
        food_list = Food.objects.all().order_by('-quantity')[:10]

        response = HttpResponse()

        heading1 = '<p>' + 'List of Fruits:' + '</p>'
        response.write(heading1)
        for fruits in food_list:
            para = '<p>' + str(fruits) + '</p>'
            response.write(para)
