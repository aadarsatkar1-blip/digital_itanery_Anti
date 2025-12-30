# itanery_app/admin.py

from django.contrib import admin
from django.contrib.admin.models import LogEntry  # ✅ ADD THIS LINE
from django.utils.html import format_html
import nested_admin
from .models import (
    Customer, Hotel, Flight, Itinerary, ItineraryDetail,
    Video, PackageInclusion, PackageExclusion, WhatsAppConfig
)


# ============= DISABLE ADMIN LOGGING =============  # ✅ ADD THIS SECTION

class NoLoggingMixin:
    """Disable all admin action logging to save database space"""
    
    def log_addition(self, request, object, message):
        pass
    
    def log_change(self, request, object, message):
        pass
    
    def log_deletion(self, request, object, message):
        pass


# ============= NESTED INLINES =============

# Activity Details inline (nested under Itinerary)
class ItineraryDetailInline(nested_admin.NestedStackedInline):
    model = ItineraryDetail
    extra = 0
    can_delete = True
    
    fields = [
        ('time','activity'),
    ]


# Itinerary Days inline with nested Activity Details
class ItineraryInline(nested_admin.NestedStackedInline):
    model = Itinerary
    extra = 0
    can_delete = True
    
    fields = [
        ('day', 'icon'),
        'title',
        'description',
    ]
    
    inlines = [ItineraryDetailInline]


# ============= REGULAR INLINES =============

class HotelInline(nested_admin.NestedStackedInline):
    model = Hotel
    extra = 0
    can_delete = True
    
    fields = [
        'name',
        ('room_type', 'stars'),
        'nights',
        'image',
        'map_url',
        'order',
    ]


class FlightInline(nested_admin.NestedStackedInline):
    model = Flight
    extra = 1
    can_delete = True
    
    fields = [
        'flight_type',
        ('from_location', 'to_location'),
        ('date', 'time'),
        ('airline', 'flight_number'),
        'cabin',
    ]


class VideoInline(nested_admin.NestedStackedInline):
    model = Video
    extra = 0
    max_num = 1
    fields = ['title', 'local_src']
    can_delete = True


class PackageInclusionInline(nested_admin.NestedTabularInline):
    model = PackageInclusion
    extra = 0
    can_delete = True
    
    fields = ['item', 'order']
    sortable_field_name = 'order'
    
    verbose_name = "Inclusion"
    verbose_name_plural = "What's Included"


class PackageExclusionInline(nested_admin.NestedTabularInline):
    model = PackageExclusion
    extra = 0
    can_delete = True
    
    fields = ['item', 'order']
    sortable_field_name = 'order'
    
    verbose_name = "Exclusion"
    verbose_name_plural = "What's Not Included"


class WhatsAppConfigInline(nested_admin.NestedStackedInline):
    model = WhatsAppConfig
    extra = 0
    max_num = 1
    fields = ['phone', 'message']
    can_delete = True


# ============= MAIN CUSTOMER ADMIN =============

@admin.register(Customer)
class CustomerAdmin(NoLoggingMixin, nested_admin.NestedModelAdmin):  # ✅ ADD NoLoggingMixin
    list_display = ['name', 'destination','slug', 'dates', 'guests', 'view_itinerary']
   
    search_fields = ['name', 'slug', 'destination', 'dates', 'guests']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('📋 Customer Information', {
            'fields': ('name', 'destination', 'dates', 'guests', 'slug'),
            'classes': ('wide',),
        }),
        ('⚙️ System Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        HotelInline,
        FlightInline,
        VideoInline,
        ItineraryInline,
        PackageInclusionInline,
        PackageExclusionInline,
        WhatsAppConfigInline,
    ]
    
    def view_itinerary(self, obj):
        url = f"/itinerary/{obj.slug}/"
        return format_html('<a href="{}" target="_blank" style="color: #0ea5e9; font-weight: bold;">🔗 View Live</a>', url)
    view_itinerary.short_description = 'Live Itinerary'


# ============= HIDE LOG ENTRY FROM ADMIN =============  # ✅ ADD THIS SECTION

try:
    admin.site.unregister(LogEntry)
except admin.sites.NotRegistered:
    pass


# ❌ NO OTHER ADMIN REGISTRATIONS
# All models are managed through Customer page only!
