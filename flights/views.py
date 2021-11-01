from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Flight, Airport, Passenger
# Create your views here.


def index(request):
    return render(request, "flights/layout.html", {
        "flights": Flight.objects.all(),
    })

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id) # pk (primary key)
    except Flight.DoesNotExist:
        # return HttpResponse(status=404)
        raise Http404("flight does not exist")
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passenger.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })



def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))