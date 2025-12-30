# itanery_app/views.py

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Customer

# Home page - Only for logged-in superusers, others get 404
def home(request):
    # Check if user is logged in AND is superuser
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise Http404("Page not found")
    
    customers = Customer.objects.all().order_by('-created_at')
    context = {
        'customers': customers
    }
    return render(request, 'itinerary/home.html', context)


# Customer itinerary - Public with direct link
def customer_itinerary(request, slug):
    customer = get_object_or_404(Customer, slug=slug)
    
    # Prepare hotels data
    hotels = []
    for hotel in customer.hotels.all():
        hotels.append({
            'name': hotel.name,
            'image': hotel.image,
            'nights': hotel.nights,
            'roomType': hotel.room_type,
            'stars': hotel.stars,
            'mapUrl': hotel.map_url,
        })
    
    # Prepare flights data
    flights = {}
    for flight in customer.flights.all():
        flight_data = {
            'from': flight.from_location,
            'to': flight.to_location,
            'date': flight.date,
            'time': flight.time,
            'airline': flight.airline,
            'flightNumber': flight.flight_number,
            'cabin': flight.cabin,
        }
        flights[flight.flight_type] = flight_data
    
    # Prepare itinerary days
    itinerary = []
    for day in customer.itinerary.all():
        details = []
        for detail in day.details.all():
            details.append({
                'time': detail.time,
                'activity': detail.activity,
            })
        
        itinerary.append({
            'day': day.day,
            'icon': day.icon,
            'title': day.title,
            'description': day.description,
            'details': details,
        })
    
    # Video
    video = None
    if hasattr(customer, 'video'):
        video = {
            'title': customer.video.title,
            'localSrc': customer.video.local_src,
        }
    
    # Inclusions
    includes = None
    if customer.inclusions.exists():
        includes = {
            'title': "What's Included",
            'items': [inc.item for inc in customer.inclusions.all()]
        }
    
    # Exclusions
    excludes = None
    if customer.exclusions.exists():
        excludes = {
            'title': "What's Not Included",
            'items': [exc.item for exc in customer.exclusions.all()]
        }
    
    # WhatsApp
    whatsapp = None
    if hasattr(customer, 'whatsapp'):
        whatsapp = {
            'phone': customer.whatsapp.phone,
            'message': customer.whatsapp.message,
        }
    
    # Build context
    context = {
        'data': {
            'client': {
                'name': customer.name,
                'destination': customer.destination,
                'dates': customer.dates,
                
                'guests': customer.guests,
            },
            'hotels': hotels,
            'flights': flights,
            'itinerary': itinerary,
            'video': video,
            'includes': includes,
            'excludes': excludes,
            'whatsapp': whatsapp,
        },
        'current_year': 2025,
        'flight_count': len(flights),
    }
    
    return render(request, 'itinerary/index.html', context)
