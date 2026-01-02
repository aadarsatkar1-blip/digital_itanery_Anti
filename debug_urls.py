
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_itanery.settings')
django.setup()

from itanery_app.models import Customer
try:
    c = Customer.objects.filter(slug__icontains='xyz').first()
    if c:
        print(f"Customer: {c.name} ({c.slug})")
        for h in c.hotels.all():
            print(f"Hotel: {h.name}")
            print(f"URL: '{h.image}'")
    else:
        print("Customer 'xyz' not found.")
except Exception as e:
    print(e)
