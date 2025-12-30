# itanery_app/models.py


from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string



class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Customer Name")
    destination = models.CharField(max_length=200, verbose_name="Destination")
    dates = models.CharField(max_length=100, verbose_name="Travel Dates")
    guests = models.CharField(max_length=100, verbose_name="Number of Guests")
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Create base slug from name
            base_slug = slugify(self.name)
            slug = base_slug
            
            # Check if slug already exists, add random string if needed
            counter = 1
            while Customer.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{get_random_string(4).lower()}"
                counter += 1
                if counter > 10:  # Safety limit
                    break
            
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['-created_at']



class Hotel(models.Model):
    customer = models.ForeignKey(Customer, related_name='hotels', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Hotel Name")
    image = models.URLField(verbose_name="Image URL", help_text="External image URL")
    nights = models.CharField(max_length=50, help_text="e.g., 3 Nights", verbose_name="Number of Nights")
    room_type = models.CharField(max_length=100, verbose_name="Room Type", help_text="e.g., Deluxe Suite")
    stars = models.IntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)], verbose_name="Star Rating")
    map_url = models.URLField(verbose_name="Google Maps URL")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    
    def __str__(self):
        return f"{self.name} - {self.customer.name}"
    
    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"
        ordering = ['order']  # ✅ CORRECT - Has 'order' field



class Flight(models.Model):
    CABIN_CHOICES = [
        ('Economy', 'Economy'),
        ('Premium Economy', 'Premium Economy'),
        ('Business', 'Business'),
        ('First Class', 'First Class'),
    ]
    
    FLIGHT_TYPE_CHOICES = [
        ('departure', 'Departure'),
        ('flight2', 'Connecting Flight'),
        ('return', 'Return'),
    ]
    
    customer = models.ForeignKey(Customer, related_name='flights', on_delete=models.CASCADE)
    flight_type = models.CharField(max_length=20, choices=FLIGHT_TYPE_CHOICES, verbose_name="Flight Type")
    from_location = models.CharField(max_length=100, verbose_name="From (City/Airport)")
    to_location = models.CharField(max_length=100, verbose_name="To (City/Airport)")
    date = models.CharField(max_length=100, verbose_name="Flight Date")
    time = models.CharField(max_length=50, verbose_name="Flight Time")
    airline = models.CharField(max_length=100, verbose_name="Airline")
    flight_number = models.CharField(max_length=50, verbose_name="Flight Number")
    cabin = models.CharField(max_length=20, choices=CABIN_CHOICES, default='Economy', verbose_name="Cabin Class")
    
    def __str__(self):
        return f"{self.get_flight_type_display()} - {self.customer.name}"
    
    class Meta:
        verbose_name = "Flight"
        verbose_name_plural = "Flights"
        ordering = ['date', 'time']  # ✅ FIXED - Order by date & time (NO 'order' field)



class Itinerary(models.Model):
    customer = models.ForeignKey(Customer, related_name='itinerary', on_delete=models.CASCADE)
    day = models.IntegerField(verbose_name="Day Number")
    icon = models.CharField(max_length=10, default='📍', help_text="Emoji icon (e.g., 🏛️, 🕌, 🛍️)")
    title = models.CharField(max_length=200, verbose_name="Day Title")
    description = models.TextField(verbose_name="Day Description")
    
    def __str__(self):
        return f"Day {self.day} - {self.customer.name}"
    
    class Meta:
        verbose_name = "Itinerary Day"
        verbose_name_plural = "Itinerary Days"
        ordering = ['day']  # ✅ FIXED - Order by day number (NO 'order' field)
        unique_together = ['customer', 'day']  # Prevent duplicate day numbers



class ItineraryDetail(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name='details', on_delete=models.CASCADE)
    time = models.CharField(max_length=50, verbose_name="Time")
    activity = models.TextField(verbose_name="Activity Description")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    
    def __str__(self):
        return f"{self.time} - {self.activity[:30]}"
    
    class Meta:
        verbose_name = "Activity Detail"
        verbose_name_plural = "Activity Details"
        ordering = ['order']  # ✅ CORRECT - Has 'order' field



class Video(models.Model):
    customer = models.OneToOneField(Customer, related_name='video', on_delete=models.CASCADE)
    title = models.CharField(
        max_length=200, 
        default='Experience a Glimpse of Your Journey',
        verbose_name="Video Title"
    )
    local_src = models.CharField(
        max_length=500, 
        help_text="Path: /static/videos/tour.mp4 or external URL",
        verbose_name="Video Source Path"
    )
    
    def __str__(self):
        return f"Video - {self.customer.name}"
    
    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"



class PackageInclusion(models.Model):
    customer = models.ForeignKey(Customer, related_name='inclusions', on_delete=models.CASCADE)
    item = models.CharField(max_length=300, verbose_name="Included Item")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    
    def __str__(self):
        return self.item
    
    class Meta:
        verbose_name = "Package Inclusion"
        verbose_name_plural = "Package Inclusions"
        ordering = ['order']  # ✅ CORRECT - Has 'order' field



class PackageExclusion(models.Model):
    customer = models.ForeignKey(Customer, related_name='exclusions', on_delete=models.CASCADE)
    item = models.CharField(max_length=300, verbose_name="Excluded Item")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    
    def __str__(self):
        return self.item
    
    class Meta:
        verbose_name = "Package Exclusion"
        verbose_name_plural = "Package Exclusions"
        ordering = ['order']  # ✅ CORRECT - Has 'order' field



class WhatsAppConfig(models.Model):
    customer = models.OneToOneField(Customer, related_name='whatsapp', on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=20, 
        help_text="Format: 919876543210 (country code + number, no spaces)",
        verbose_name="WhatsApp Phone Number"
    )
    message = models.TextField(
        default='I want to finalize this itinerary!',
        verbose_name="Default Message"
    )
    
    def __str__(self):
        return f"WhatsApp - {self.customer.name}"
    
    class Meta:
        verbose_name = "WhatsApp Configuration"
        verbose_name_plural = "WhatsApp Configurations"
