# itanery_app/urls.py

from django.urls import path
from . import views

app_name = 'itanery_app'

urlpatterns = [
    path('', views.home, name='home'),  # ✅ Admin only, others 404
    path('itinerary/<slug:slug>/', views.customer_itinerary, name='customer_itinerary'),
]

