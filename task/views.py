from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
import datetime

# Create your views here.


def index(request):
   
    form = TaskForm()
    if request.user.is_authenticated:
        user = request.user
        list = Task.objects.filter(user= user)
        
            
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                adding_user = form.save(commit=False)
                adding_user.user = user
                adding_user.save()
                form.save()
            return redirect("/")   
        return render(request,'task.html',{'list' : list, 'form' : form})
    else:
        messages.info(request,"Firstly login to create or view your list")
        return render(request,'task.html', {'form' : form})




def update(request,x):
    list = Task.objects.get(id=x)
    form = TaskForm(instance=list)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=list)
       
       
        if form.is_valid():
            form.save()
            return redirect("/")   
    return render(request,'update.html',{'form' : form})



def delete(request,y):
    item = Task.objects.get(id=y)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    return render(request,'delete.html',{'item' : item})    




def signup(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        email     = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username = user_name).exists():
                messages.info(request,'username taken')
                return redirect('signup')
            elif User.objects.filter(email = email).exists():
                messages.info(request,'email taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=user_name, password=password1,email=email)
                user.save()
                messages.info(request,'account created')
                return redirect('signup')
        else:
            messages.info(request,'password not matching')
            return redirect('signup')
        return redirect('/')
    else:
        return render(request,'signup.html')    



    

def login(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,"Invalid username or password")    
            return redirect('login')
    else:
        return render(request,'login.html')



def logout(request):
    auth.logout(request)
    return redirect('/')
