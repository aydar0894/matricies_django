from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
# from PRIPS_workflow import run_workflow
from MatrixCalculation import MultiplierCorrelationCalculator, MongoConnector
import json
from pymongo import MongoClient



class MatrixForm(forms.Form):
    horizon = forms.CharField()
    currencies_list = forms.CharField()
    return_frequency = forms.CharField()

@csrf_exempt
def matrix(request):
    MONGO_DB_NAME       = 'bitcoin'
    MONGO_HOST       = 'localhost'
    MONGO_COLLECTIONS        = ['daily_data', 'hourly_data']
    MONGO_DB_DEFAULT_COLLECTION = 'daily_data'
    if request.method == 'POST':
        form = MatrixForm(request.POST)
        # pprint(request.form)
        if form.is_valid():
            horizon          = int(form.cleaned_data['horizon'])
            currencies_list  = form.cleaned_data['currencies_list'].split(',')
            return_frequency = form.cleaned_data['return_frequency']
            print(horizon)
            print(currencies_list)
            print(return_frequency)
            p_frequency = ['dayily', 'hourly']
            if return_frequency not in p_frequency:
                return_frequency = 'daily'
            data = MultiplierCorrelationCalculator(horizon=horizon,
                                            currencies_list=currencies_list,
                                            return_frequency=return_frequency,
                                            db_name=MONGO_DB_NAME
                                            ).calculate_pairs()

            return JsonResponse(data, safe=False)
@csrf_exempt
def currencies(request):
    MONGO_DB_NAME       = 'bitcoin'
    MONGO_HOST       = 'localhost'
    MONGO_COLLECTIONS        = ['daily_data', 'hourly_data']
    MONGO_DB_DEFAULT_COLLECTION = 'daily_data'
    if request.method == 'POST':

        selected_params   = {}, {'Ccy': 1, '_id': 0}
        connector  = MongoClient(host=MONGO_HOST,
                                 authSource=MONGO_DB_NAME)
        collection = connector[MONGO_DB_NAME][MONGO_DB_DEFAULT_COLLECTION]
        data       = list([x['Ccy'] for x in collection.find(*selected_params)])

        return JsonResponse(data, safe=False)

# Create your views here.
