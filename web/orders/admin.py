from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Profile

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_first_name', 'get_last_name', 'get_city',
                    'paid','created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_city(self, obj):
        return obj.user.profile.city

    get_first_name.short_description = 'First name'
    get_last_name.short_description = 'Last name'
    get_city.short_description = 'City'
