from django.shortcuts import render

from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Register
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

global username, unique_df

def ViewVotersAction(request):
    if request.method == 'POST':
        voter_id = request.POST.get('t1', False)
        dataset = pd.read_excel('DataVoter.xlsx')
        search_data = dataset.loc[dataset['VoterId'] == voter_id]
        output = voter_id+" doesn't exists"
        if len(search_data) > 0:
            output = '<table border=1 align=center width=100%><tr><th><font size="3" color="black">Name</th><th><font size="3" color="black">Father/Husband</th><th><font size="3" color="black">Age</th><th><font size="3" color="black">Gender</th>'
            output+='<th><font size="3" color="black">Voter ID</th><th><font size="3" color="black">Aadhar No</th></tr>'
            search_data = search_data.values
            for i in range(len(search_data)):
                output += '<td><font size="3" color="black">'+str(search_data[i,0])+'</td>'
                output += '<td><font size="3" color="black">'+str(search_data[i,1])+'</td>'
                output += '<td><font size="3" color="black">'+str(search_data[i,2])+'</td>'
                output += '<td><font size="3" color="black">'+str(search_data[i,3])+'</td>'
                output += '<td><font size="3" color="black">'+str(search_data[i,4])+'</td>'
                output += '<td><font size="3" color="black">'+str(search_data[i,5])+'</td></tr>'
        context= {'data':output}
        return render(request, 'ViewResult.html', context)
            
def Download(request):
    if request.method == 'GET':
        name = "unique.xlsx"
        with open(name, mode="rb") as excel:
            data = excel.read()
        excel.close()
        response = HttpResponse(data,content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename='+name
        return response 

def RemoveDuplicate(request):
    if request.method == 'GET':
        global unique_df
        dataset = pd.read_excel('DataVoter.xlsx')
        total_records = dataset.shape[0]
        unique_df = dataset.drop_duplicates(subset=["VoterId"], keep=False)
        unique_records = unique_df.shape[0]
        unique_df.to_excel("unique.xlsx", index=False)
        output = "Total records before Deduplication : "+str(total_records)+"<br/>Total records after Deduplication : "+str(unique_records)
        context= {'data': output}
        height = [total_records, unique_records]
        bars = ('Before Deduplication Count','After Deduplication Count')
        y_pos = np.arange(len(bars))
        plt.bar(y_pos, height)
        plt.xticks(y_pos, bars)
        plt.xlabel("Type")
        plt.ylabel("Count")
        plt.title("Count Before & After Deduplication")
        plt.show()
        return render(request, 'UserScreen.html', context)

def AddNewVoter(request):
    if request.method == 'GET':
       return render(request, 'AddNewVoter.html', {})

def AddNewVoterAction(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        father = request.POST.get('t2', False)
        age = request.POST.get('t3', False)
        gender = request.POST.get('t4', False)
        voter = request.POST.get('t5', False)
        aadhar = request.POST.get('t6', False)
        print("==========="+father);
        dataset = pd.read_excel('DataVoter.xlsx')
        new_rec = {'Name': name, 'Father_Husband': father, 'Age': age, 'Gender': gender, 'VoterId': voter, 'Aadhar no': aadhar}
        new_df = pd.DataFrame([new_rec])
        dataset = pd.concat([dataset, new_df], ignore_index=True)
        dataset.to_excel('DataVoter.xlsx', index=False)
        context= {'data':'New record added to existing DataVoter.xlsx<br/>You can open & verify that xlsx file'}
        return render(request, 'AddNewVoter.html', context) 

def ViewVoters(request):
    if request.method == 'GET':
       return render(request, 'ViewVoters.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})   

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        
        # Check if username already exists
        if Register.objects.filter(username=username).exists():
            context = {'data': 'Username already exists'}
            return render(request, 'Register.html', context)
        
        # Create new user
        try:
            Register.objects.create(
                username=username,
                password=password,
                contact=contact,
                email=email,
                address=address
            )
            context = {'data': 'Signup Process Completed'}
            return render(request, 'Register.html', context)
        except Exception as e:
            context = {'data': 'Error in signup process: ' + str(e)}
            return render(request, 'Register.html', context) 
        
def UserLogin(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        
        # Check if user exists with matching credentials
        try:
            user = Register.objects.get(username=username, password=password)
            context = {'data': 'welcome ' + username}
            return render(request, 'UserScreen.html', context)
        except Register.DoesNotExist:
            context = {'data': 'Invalid login details'}
            return render(request, 'Login.html', context)        
        
        
