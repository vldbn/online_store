import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from orders.models import Order, OrderItem


def export_to_csv(modelAdmin, request, queryset):
    opts = modelAdmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' \
                                      f'filename={opts.verbose_name}.csv'
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if
              not field.many_to_many and not field.one_to_many]
    # labels of table
    writer.writerow([field.verbose_name for field in fields])
    # write data by row
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_first_name', 'get_last_name', 'get_city',
                    'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_city(self, obj):
        return obj.user.profile.city

    get_first_name.short_description = 'First name'
    get_last_name.short_description = 'Last name'
    get_city.short_description = 'City'
