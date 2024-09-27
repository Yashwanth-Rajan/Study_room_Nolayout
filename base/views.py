from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages        #handle error 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required  #restrict users
from django.contrib.auth import authenticate ,login ,logout #authentication
from django.db.models import Q #select multiple filters
from .models import Room ,Topic,Message
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm


# rooms=[
#     {'id':1,"name":"Python community classroom"},
#      {'id':2,"name":"Design with yash"},
#       {'id':3,"name":"DSA"}
# ]

def loginPage(request):
    page="login"
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist...!!!")
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user) #creates a session in browser & database
            return redirect('home')
        else:
            messages.error(request,'username  or password does not exist')
        
    context = {'page':page}
    return render(request,'base/login_register.html',context)


def logoutUser(request):
    logout(request) #deletes the session token
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)#pass the data in the form
        if form.is_valid():
            user = form.save(commit=False) #here we save the form and freeze it to process it further.
            user.username=user.username.lower()
            user.save() #this saves the form to database.
            login(request,user) #after saving we login the user
            return redirect('home')
        else:
            messages.error(request,"An error occurred during registration")

    return render(request,'base/login_register.html',{'form':form})


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    context={"user":user}
    return render(request,'base/profile.html',context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms=Room.objects.filter(
       Q(topic__name__icontains=q)|
       Q(name__icontains=q)|
       Q(description__icontains=q)
        ) 
    topics = Topic.objects.all()
    room_count= rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context={'rooms':rooms,'topics':topics,'room_count':room_count , "room_messages":room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() #It queries messages of that particular room from the child in model(Message)
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)#adds the user to participants
        return redirect('room',pk=room.id)

    context = {'room':room ,'room_messages':room_messages,'participants':participants }
    return render(request,'base/room.html',context)



@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST' :
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') #we have name(home) in the urls so it can be accessed
    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    context={'form':form}

    if request.user != room.host:
        return HttpResponse("you are not allowed")
    
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!! ')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!! ')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})