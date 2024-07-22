from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import *
from django import forms

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("loginView"))
    
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def fligth(request, flight_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("loginView"))
    
    flight = Flight.objects.get(id=flight_id)
    passangers = flight.passengers.all()
    non_passengers = Passanger.objects.exclude(flights = flight).all()
    return render(request, "flights/flight.html", {
        "flights": flight,
        "passangers": passangers,
        "non_passengers": non_passengers
    })

def book(request, flight_id):

    # For a post request, add a new flight
    if request.method == "POST":

        # Accessing the flight
        flight = Flight.objects.get(pk=flight_id)

        # Finding the passenger id from the submitted form data
        passenger_id = int(request.POST["passenger"])

        # Finding the passenger based on the id
        passenger = Passanger.objects.get(pk=passenger_id)

        # Add passenger to the flight
        passenger.flights.add(flight)

        # Redirect user to flight page
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
    
def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "flights/login.html",{
                "message": "Invalid Credentials",
                "loginForm": LoginForm()
            })
    return render(request, "flights/login.html", {
        "loginForm": LoginForm()
    })

def logoutView(request):
    logout(request)
    return render(request, "flights/login.html", {
        "loginForm": LoginForm()
    })

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class':'form-control'}
    ))