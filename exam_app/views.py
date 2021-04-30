from django.shortcuts import render, redirect
from .models import User,Wish
from django.contrib import messages
import bcrypt

def index(request):
    if 'uid' in request.session:
        return redirect('/wishes')
    return render(request,"index.html")

def register(request):
    # validate then create user
    if request.method=='POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        ###########ELSE##############
        # create the hash    
        password = request.POST['pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
        print(pw_hash)
        user=User.objects.create(first_name=request.POST['fname'],
                            last_name=request.POST['lname'],
                            Email=request.POST['email'],
                            password=pw_hash)
        request.session['uid']=user.id
        return redirect('/wishes')

def welcome(request):
    #do things
    context={
        'user':User.objects.get(id= request.session['uid']),
        'all_wishes':Wish.objects.all()
    }
    return render(request,'wishes.html',context)



def new_wish(request):
    return render(request,'new_wish.html')

def add_wish(request):
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/wishes/new")
        Wish.objects.create(
                item=request.POST['item'],
                description=request.POST['desc'],
                granted='False',
                wisher=User.objects.get(id=request.session['uid'])
            )
    return redirect("/wishes")

def cancel(request):
    return redirect("/wishes")


def remove_wish(request,w_id):
    wish = Wish.objects.get(id=w_id)
    wish.delete()
    return redirect("/wishes")


def edit_wish(request, w_id):
    context = {
        'wish': Wish.objects.get(id=w_id)
    }
    return render(request, "edit.html", context)

def update_wish(request,w_id):
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/wishes/new")
        granted = False
        wish=Wish.objects.get(id=w_id)
        wish.item = request.POST['item']
        wish.description = request.POST['desc']
        wish.save()
    return redirect("/wishes")


def granted_wish(request,w_id):
    user = User.objects.get(id=request.session['uid'])
    wish=Wish.objects.get(id=w_id)
    wish.granted='True'
    wish.granted_for.add(user)
    wish.save()
    return redirect("/wishes")


def make_like(request,w_id):
    user = User.objects.get(id=request.session['uid'])
    wish = Wish.objects.get(id=w_id)
    wish.liked_by.add(user)
    return redirect("/wishes")

def view_stats(request):
    all_granted=Wish.objects.filter(granted='True')
    logged_user_granted=Wish.objects.filter(granted='True', wisher=User.objects.get(id=request.session['uid']))
    logged_user_pending=Wish.objects.filter(granted='False', wisher=User.objects.get(id=request.session['uid']))
    context={
    'user':User.objects.get(id=request.session['uid']),
    'all_granted':all_granted,
    'logged_user_granted':logged_user_granted,
    'logged_user_pending':logged_user_pending
    }
    return render(request,'view_stats.html',context)


def login(request):
    if request.method=='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        ###########ELSE##############
        user = User.objects.filter(Email=request.POST['email']) # why are we using filter here instead of get?
        if user: # note that we take advantage of truthiness here: an empty list will return false
            logged_user = user[0] 
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['uid'] = logged_user.id
                # never render on a post, always redirect!
                return redirect('/wishes')
        # if we didn't find anything in the database by searching by username or if the passwords don't match, 
        # redirect back to a safe route
        return redirect("/")

def logout(request):
    request.session.flush()
    return redirect('/')