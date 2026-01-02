# itanery_app/admin.py

from django.contrib import admin
from django.utils.html import format_html
import nested_admin
from .models import (
    Customer, Hotel, Flight, Itinerary, ItineraryDetail,
    Video, PackageInclusion, PackageExclusion, WhatsAppConfig
)


# ============= NESTED INLINES =============

# Activity Details inline (nested under Itinerary)
class ItineraryDetailInline(nested_admin.NestedTabularInline):
    model = ItineraryDetail
    extra = 0
    can_delete = True
    
    fields = [
        'time','activity',
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

class HotelInline(nested_admin.NestedTabularInline):
    model = Hotel
    extra = 0
    can_delete = True
    
    fields = [
        'name',
        'room_type', 
        'stars',
        'nights',
        'image',
        'map_url',
        'order',
    ]


class FlightInline(nested_admin.NestedTabularInline):
    model = Flight
    extra = 0
    can_delete = True
    
    fields = [
        'flight_type',
        'from_location',
        'to_location',
        'date',
        'time',
        'airline',
        'flight_number',
        'cabin',
    ]


class VideoInline(nested_admin.NestedTabularInline):
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


class WhatsAppConfigInline(nested_admin.NestedTabularInline):
    model = WhatsAppConfig
    extra = 0
    max_num = 1
    fields = ['phone', 'message']
    can_delete = True


# ============= MAIN CUSTOMER ADMIN =============

from django.db import transaction

@admin.register(Itinerary)
class ItineraryAdmin(nested_admin.NestedModelAdmin):
    list_display = ['day', 'title', 'customer', 'get_day_detail']
    list_filter = ['customer']
    search_fields = ['title', 'description', 'customer__name']
    ordering = ['customer', 'day']
    inlines = [ItineraryDetailInline]
    
    def get_day_detail(self, obj):
        return f"{obj.details.count()} activities"
    get_day_detail.short_description = 'Activities'

@admin.register(Customer)
class CustomerAdmin(nested_admin.NestedModelAdmin):
    list_display = ['name', 'destination','slug', 'dates', 'guests', 'view_itinerary_link']
   
    search_fields = ['name', 'slug', 'destination', 'dates', 'guests']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at', 'view_all_itinerary_days']
    
    fieldsets = (
        ('📋 Customer Information', {
            'fields': ('name', 'destination', 'dates', 'guests', 'slug'),
            'classes': ('wide',),
        }),
        ('📅 Itinerary Management', {
            'fields': ('view_all_itinerary_days',),
            'description': 'Manage the Day-wise Itinerary for this customer here.',
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
        # ItineraryInline,  <-- REMOVED to save memory. Manage via separate page.
        PackageInclusionInline,
        PackageExclusionInline,
        WhatsAppConfigInline,
    ]
    
    @transaction.atomic
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related(
            'hotels',
            'flights',
            'video',
            'inclusions',
            'exclusions',
            'whatsapp'
        )

    def view_itinerary_link(self, obj):
        url = f"/itinerary/{obj.slug}/"
        return format_html('<a href="{}" target="_blank" style="color: #0ea5e9; font-weight: bold;">🔗 View Live</a>', url)
    view_itinerary_link.short_description = 'Live Itinerary'
    
    def view_all_itinerary_days(self, obj):
        count = obj.itinerary.count()
        url = f"/admin/itanery_app/itinerary/?customer__id__exact={obj.id}"
        return format_html(
            '<a class="button" href="{}" style="background-color: #4f46e5; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;">'
            '📅 Manage {} Days of Itinerary</a>', 
            url, count
        )
    view_all_itinerary_days.short_description = "Itinerary Days"


# ❌ NO OTHER ADMIN REGISTRATIONS
# All models are managed through Customer page only!
