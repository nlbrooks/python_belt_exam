from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "belt_app/index.html")

def create_user(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']
            email = request.POST['email']
            pw = request.POST['password']
            pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            this_user = User.objects.create(first_name=f_name, last_name=l_name, email=email, password=pw_hash)
            request.session['user'] = this_user.id
            return redirect("/dashboard")


def login(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            email = request.POST['email']
            this_user = User.objects.get(email=email)
            request.session['user'] = this_user.id
            return redirect("/dashboard")



def logout(request):
    if 'user' in request.session:
        request.session.pop('user')
    return redirect('/')


def dashboard(request):
    if 'user' in request.session:
        this_user = User.objects.get(id=request.session['user'])
        user_joins = Join.objects.filter(user=this_user)
        context = {
            "this_user": User.objects.get(id=request.session['user']),
            "all_users": User.objects.all(),
            "all_trips": Trip.objects.all(),
            "all_joins": Join.objects.all(),
            "user_joins": user_joins,
        } 
        return render(request, "belt_app/dashboard.html", context)
    else:
        return redirect('/')


def new_trip(request):
    if 'user' in request.session: 
        context = {
            "this_user": User.objects.get(id=request.session['user']),
        }
        return render(request, "belt_app/create_trip.html", context)
    else:
        return redirect('/')


def create_trip(request):
    if request.method == 'GET':
        return redirect("/dashboard")
    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/trips/new")
        else:
            form_dest = request.POST['destination']
            form_start = request.POST['start_date']
            form_end = request.POST['end_date']
            form_plan = request.POST['plan']
            form_creator = request.POST['creator']
            trip_creator = User.objects.get(id=form_creator)
            Trip.objects.create(destination=form_dest, start_date=form_start, end_date=form_end, plan=form_plan, creator=trip_creator)
            return redirect("/dashboard")


def edit(request, my_val):
    if 'user' in request.session:
        this_trip = Trip.objects.get(id=my_val)
        st_date = this_trip.start_date
        ed_date = this_trip.end_date
        fm_st_date = st_date.strftime("%Y-%m-%d")
        fm_ed_date = ed_date.strftime("%Y-%m-%d")
        context = {
            "this_user": User.objects.get(id=request.session['user']),
            "trip": this_trip,
            "st_date": fm_st_date,
            "ed_date": fm_ed_date,
        }
        return render(request, "belt_app/edit_trip.html", context)
    else:
        return redirect('/')


def edit_trip(request):
    if request.method == 'GET':
        return redirect("/shows")
    if request.method == 'POST':
        form_trip_id = request.POST['trip_id']
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/trips/edit/{form_trip_id}")
        else:
            form_dest = request.POST['destination']
            form_start = request.POST['start_date']
            form_end = request.POST['end_date']
            form_plan = request.POST['plan']
            this_trip = Trip.objects.get(id=form_trip_id)
            this_trip.destination = form_dest
            this_trip.start_date = form_start
            this_trip.end_date = form_end
            this_trip.plan = form_plan
            this_trip.save()
            return redirect("/dashboard")


def show_trip(request, my_val):
    if 'user' in request.session:
        this_trip = Trip.objects.get(id=my_val)
        st_date = this_trip.start_date
        ed_date = this_trip.end_date
        c_date = this_trip.created_at
        u_date = this_trip.updated_at
        fm_c_date = c_date.strftime("%m/%d/%y")
        fm_u_date = u_date.strftime("%m/%d/%y")
        fm_st_date = st_date.strftime("%m/%d/%y")
        fm_ed_date = ed_date.strftime("%m/%d/%y")
        context = {
            "this_user": User.objects.get(id=request.session['user']),
            "this_trip": this_trip,
            "st_date": fm_st_date,
            "ed_date": fm_ed_date,
            "c_date": fm_c_date,
            "u_date": fm_u_date,
            "all_joins": Join.objects.all(),
        }
        return render(request, "belt_app/show_trip.html", context)
    else:
        return redirect('/')


def remove(request, my_val):
    if 'user' in request.session:
        this_user = User.objects.get(id=request.session['user'])
        this_trip = Trip.objects.get(id=my_val)
        if this_trip.creator == this_user:
            this_trip.delete()
        return redirect('/dashboard')
    else:
        return redirect('/')


def join(request, my_val):
    if 'user' in request.session:
        this_user = User.objects.get(id=request.session['user'])
        this_trip = Trip.objects.get(id=my_val)
        if this_trip.creator != this_user:
            db_list = Join.objects.filter(user=this_user, trip=this_trip)
            if len(db_list) == 0:
                Join.objects.create(user=this_user, trip=this_trip)
        return redirect('/dashboard')
    else:
        return redirect('/')


def cancel(request, my_val):
    if 'user' in request.session:
        this_user = User.objects.get(id=request.session['user'])
        this_trip = Trip.objects.get(id=my_val)
        this_join = Join.objects.filter(user=this_user, trip=this_trip)
        this_join.delete()
        return redirect('/dashboard')
    else:
        return redirect('/')